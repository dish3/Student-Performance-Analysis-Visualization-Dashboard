# ============================================================
# analytics.py  –  SQL query functions for advanced analytics
# All Decimal/float values are cast to Python float before
# returning so they are safely JSON-serialisable.
# ============================================================


def _f(val, default=0.0):
    """Safely cast a DB value (Decimal / None) to float."""
    return float(val) if val is not None else float(default)


def _i(val, default=0):
    """Safely cast a DB value to int."""
    return int(val) if val is not None else int(default)


# ── Reusable per-student avg score subquery ───────────────
_STUDENT_AVG = """
    SELECT s.moodle_id, s.name, s.roll_no,
           ROUND(SUM(stm.obtained_marks) / NULLIF(SUM(tq.max_marks), 0) * 100, 2) AS avg_pct
    FROM students s
    JOIN student_test_marks stm ON s.moodle_id = stm.moodle_id
    JOIN test_questions tq      ON stm.question_id = tq.question_id
    GROUP BY s.moodle_id
"""


def get_overall_stats(conn):
    """
    Returns overall class stats:
      total_students, avg_marks_pct, avg_attendance,
      topper, pass_pct, weak_students
    """
    cur = conn.cursor(dictionary=True)

    # Total students
    cur.execute("SELECT COUNT(*) AS total FROM students")
    total_students = _i(cur.fetchone()['total'])

    # Average score % across all student-test-attempt combinations
    cur.execute(f"""
        SELECT ROUND(AVG(avg_pct), 2) AS avg_marks_pct
        FROM ({_STUDENT_AVG}) sub
    """)
    avg_marks_pct = _f(cur.fetchone()['avg_marks_pct'])

    # Average attendance percentage (from stored percentage table)
    cur.execute("SELECT ROUND(AVG(attendance_percent), 2) AS avg_att FROM attendance_percentage")
    avg_attendance = _f(cur.fetchone()['avg_att'])

    # Class topper
    cur.execute(f"""
        SELECT name, moodle_id, avg_pct
        FROM ({_STUDENT_AVG}) sub
        ORDER BY avg_pct DESC LIMIT 1
    """)
    topper_row = cur.fetchone()
    topper = {'name': topper_row['name'],
              'moodle_id': topper_row['moodle_id'],
              'avg_pct': _f(topper_row['avg_pct'])} if topper_row else None

    # Pass percentage (avg score >= 40%)
    cur.execute(f"""
        SELECT ROUND(
            SUM(CASE WHEN avg_pct >= 40 THEN 1 ELSE 0 END) /
            NULLIF(COUNT(*), 0) * 100, 2) AS pass_pct
        FROM ({_STUDENT_AVG}) sub
    """)
    pass_pct = _f(cur.fetchone()['pass_pct'])

    # Weak students (avg score < 40%)
    cur.execute(f"""
        SELECT name, moodle_id, roll_no, avg_pct
        FROM ({_STUDENT_AVG}) sub
        HAVING avg_pct < 40
        ORDER BY avg_pct ASC
    """)
    weak_students = [
        {**r, 'avg_pct': _f(r['avg_pct'])} for r in cur.fetchall()
    ]

    cur.close()
    return {
        'total_students': total_students,
        'avg_marks_pct':  avg_marks_pct,
        'avg_attendance': avg_attendance,
        'topper':         topper,
        'pass_pct':       pass_pct,
        'weak_students':  weak_students,
    }


def get_marks_analysis(conn):
    """
    Returns marks analytics:
      avg_per_test, top10, pass_fail, distribution,
      highest_per_test, comparison
    All numeric values are plain Python float/int.
    """
    cur = conn.cursor(dictionary=True)

    # Average score % per test
    cur.execute("""
        SELECT t.test_name,
               ROUND(SUM(stm.obtained_marks) /
                     NULLIF(SUM(tq.max_marks), 0) * 100, 2) AS avg_pct
        FROM student_test_marks stm
        JOIN test_questions tq ON stm.question_id = tq.question_id
        JOIN tests t           ON stm.test_id     = t.test_id
        GROUP BY t.test_id
        ORDER BY t.test_id
    """)
    avg_per_test = [
        {'test_name': r['test_name'], 'avg_pct': _f(r['avg_pct'])}
        for r in cur.fetchall()
    ]

    # Top 10 students by overall avg score %
    cur.execute(f"""
        SELECT sub.name, sub.moodle_id, sub.roll_no, sub.avg_pct,
               SUM(stm.obtained_marks) AS total_obtained,
               SUM(tq.max_marks)       AS total_max
        FROM ({_STUDENT_AVG}) sub
        JOIN student_test_marks stm ON sub.moodle_id = stm.moodle_id
        JOIN test_questions tq      ON stm.question_id = tq.question_id
        GROUP BY sub.moodle_id
        ORDER BY sub.avg_pct DESC LIMIT 10
    """)
    top10 = [
        {**r, 'avg_pct': _f(r['avg_pct']),
         'total_obtained': _i(r['total_obtained']),
         'total_max': _i(r['total_max'])}
        for r in cur.fetchall()
    ]

    # Pass vs Fail count
    cur.execute(f"""
        SELECT
            SUM(CASE WHEN avg_pct >= 40 THEN 1 ELSE 0 END) AS pass_count,
            SUM(CASE WHEN avg_pct <  40 THEN 1 ELSE 0 END) AS fail_count
        FROM ({_STUDENT_AVG}) sub
    """)
    pf_row = cur.fetchone()
    pass_fail = {
        'pass_count': _i(pf_row['pass_count']),
        'fail_count':  _i(pf_row['fail_count']),
    }

    # Marks distribution buckets
    cur.execute(f"""
        SELECT
            SUM(CASE WHEN avg_pct <  40              THEN 1 ELSE 0 END) AS b0_40,
            SUM(CASE WHEN avg_pct >= 40 AND avg_pct < 60 THEN 1 ELSE 0 END) AS b40_60,
            SUM(CASE WHEN avg_pct >= 60 AND avg_pct < 80 THEN 1 ELSE 0 END) AS b60_80,
            SUM(CASE WHEN avg_pct >= 80              THEN 1 ELSE 0 END) AS b80_100
        FROM ({_STUDENT_AVG}) sub
    """)
    d = cur.fetchone()
    distribution = {
        '0_40':   _i(d['b0_40']),
        '40_60':  _i(d['b40_60']),
        '60_80':  _i(d['b60_80']),
        '80_100': _i(d['b80_100']),
    }

    # Highest score % per test
    cur.execute("""
        SELECT t.test_name,
               ROUND(MAX(sub.pct), 2) AS highest_pct
        FROM (
            SELECT stm.test_id,
                   SUM(stm.obtained_marks) /
                   NULLIF(SUM(tq.max_marks), 0) * 100 AS pct
            FROM student_test_marks stm
            JOIN test_questions tq ON stm.question_id = tq.question_id
            GROUP BY stm.moodle_id, stm.test_id, stm.attempt_no
        ) sub
        JOIN tests t ON sub.test_id = t.test_id
        GROUP BY t.test_id
        ORDER BY t.test_id
    """)
    highest_per_test = [
        {'test_name': r['test_name'], 'highest_pct': _f(r['highest_pct'])}
        for r in cur.fetchall()
    ]

    # Per-student avg for comparison chart
    cur.execute(f"""
        SELECT name, avg_pct
        FROM ({_STUDENT_AVG}) sub
        ORDER BY avg_pct DESC
    """)
    comparison = [
        {'name': r['name'], 'avg_pct': _f(r['avg_pct'])}
        for r in cur.fetchall()
    ]

    cur.close()
    return {
        'avg_per_test':    avg_per_test,
        'top10':           top10,
        'pass_fail':       pass_fail,
        'distribution':    distribution,
        'highest_per_test':highest_per_test,
        'comparison':      comparison,
    }


def get_attendance_analysis(conn):
    """
    Returns attendance analytics:
      all_attendance, top10_att, defaulters,
      monthly_trend, pie_data
    """
    cur = conn.cursor(dictionary=True)

    # All students with attendance %
    cur.execute("""
        SELECT s.name, s.moodle_id, s.roll_no,
               COALESCE(ap.attendance_percent, 0) AS att_pct
        FROM students s
        LEFT JOIN attendance_percentage ap ON s.moodle_id = ap.moodle_id
        ORDER BY att_pct DESC
    """)
    all_attendance = [
        {**r, 'att_pct': _f(r['att_pct'])} for r in cur.fetchall()
    ]

    top10_att  = all_attendance[:10]
    defaulters = [r for r in all_attendance if r['att_pct'] < 75]

    # Monthly trend
    cur.execute("""
        SELECT DATE_FORMAT(date, '%Y-%m') AS month,
               SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END) AS present_cnt,
               SUM(CASE WHEN status='Absent'  THEN 1 ELSE 0 END) AS absent_cnt
        FROM attendance_daily
        GROUP BY month
        ORDER BY month
    """)
    monthly_trend = [
        {'month': r['month'],
         'present_cnt': _i(r['present_cnt']),
         'absent_cnt':  _i(r['absent_cnt'])}
        for r in cur.fetchall()
    ]

    # Overall present vs absent
    cur.execute("""
        SELECT
            SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END) AS total_present,
            SUM(CASE WHEN status='Absent'  THEN 1 ELSE 0 END) AS total_absent
        FROM attendance_daily
    """)
    pd_row = cur.fetchone()
    pie_data = {
        'total_present': _i(pd_row['total_present']),
        'total_absent':  _i(pd_row['total_absent']),
    }

    cur.close()
    return {
        'all_attendance': all_attendance,
        'top10_att':      top10_att,
        'defaulters':     defaulters,
        'monthly_trend':  monthly_trend,
        'pie_data':       pie_data,
    }


def get_filtered_students(conn, filter_type):
    """
    Return students filtered by filter_type.
    Safe against no-marks data (NULLIF prevents division by zero).
    """
    cur = conn.cursor(dictionary=True)

    # Base: LEFT JOINs so students with no marks still appear (avg_pct = 0)
    base = """
        SELECT s.name, s.moodle_id, s.roll_no,
               ROUND(SUM(stm.obtained_marks) /
                     NULLIF(SUM(tq.max_marks), 0) * 100, 2) AS avg_pct,
               COALESCE(ap.attendance_percent, 0) AS att_pct
        FROM students s
        LEFT JOIN student_test_marks stm ON s.moodle_id = stm.moodle_id
        LEFT JOIN test_questions tq      ON stm.question_id = tq.question_id
        LEFT JOIN attendance_percentage ap ON s.moodle_id = ap.moodle_id
        GROUP BY s.moodle_id
    """

    queries = {
        'top10':         base + " ORDER BY avg_pct DESC LIMIT 10",
        'top5':          base + " ORDER BY avg_pct DESC LIMIT 5",
        'below_avg':     base + " HAVING avg_pct < (SELECT AVG(p) FROM ("
                                "SELECT SUM(stm2.obtained_marks)/"
                                "NULLIF(SUM(tq2.max_marks),0)*100 AS p "
                                "FROM student_test_marks stm2 "
                                "JOIN test_questions tq2 ON stm2.question_id=tq2.question_id "
                                "GROUP BY stm2.moodle_id) x) ORDER BY avg_pct ASC",
        'att_below75':   base + " HAVING att_pct < 75 ORDER BY att_pct ASC",
        'marks_below40': base + " HAVING avg_pct < 40 OR avg_pct IS NULL ORDER BY avg_pct ASC",
    }

    sql = queries.get(filter_type, queries['top10'])
    cur.execute(sql)
    result = [
        {**r, 'avg_pct': _f(r['avg_pct']), 'att_pct': _f(r['att_pct'])}
        for r in cur.fetchall()
    ]
    cur.close()
    return result
