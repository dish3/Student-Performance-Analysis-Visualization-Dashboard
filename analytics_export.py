# ============================================================
# analytics_export.py  –  Multi-sheet Excel export with charts
# Uses pandas for data frames + xlsxwriter for chart embedding
# ============================================================

import io
import pandas as pd
from analytics import (
    get_overall_stats, get_marks_analysis,
    get_attendance_analysis, get_filtered_students
)


def export_full_analysis(conn):
    """
    Build a 5-sheet Excel workbook:
      Sheet 1 – Students List
      Sheet 2 – Marks Analysis
      Sheet 3 – Attendance Analysis
      Sheet 4 – Overall Class Analysis
      Sheet 5 – Charts (bar, pie, line embedded)
    Returns BytesIO ready for Flask send_file().
    """
    output = io.BytesIO()

    # Fetch all data
    overall   = get_overall_stats(conn)
    marks     = get_marks_analysis(conn)
    att       = get_attendance_analysis(conn)

    # Fetch students list
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT moodle_id, roll_no, name, moodle_email, phone FROM students ORDER BY moodle_id")
    students_list = cur.fetchall()
    cur.close()

    # Pre-compute values needed across multiple sheets
    pf = marks['pass_fail']
    dist_hdrs = ['0–40%', '40–60%', '60–80%', '80–100%']
    dist_vals = [
        marks['distribution']['0_40'],
        marks['distribution']['40_60'],
        marks['distribution']['60_80'],
        marks['distribution']['80_100'],
    ]
    avg_test_data = marks['avg_per_test']

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        wb = writer.book

        # ── Shared formats ────────────────────────────────────
        hdr_fmt = wb.add_format({
            'bold': True, 'bg_color': '#4472C4', 'font_color': '#FFFFFF',
            'align': 'center', 'valign': 'vcenter', 'border': 1
        })
        title_fmt = wb.add_format({'bold': True, 'font_size': 14, 'font_color': '#1F3864'})
        cell_fmt  = wb.add_format({'align': 'center', 'border': 1})
        pct_fmt   = wb.add_format({'num_format': '0.00"%"', 'align': 'center', 'border': 1})
        green_fmt = wb.add_format({'bg_color': '#E2EFDA', 'align': 'center', 'border': 1})
        red_fmt   = wb.add_format({'bg_color': '#FCE4D6', 'align': 'center', 'border': 1})
        stat_lbl  = wb.add_format({'bold': True, 'bg_color': '#D9E1F2', 'border': 1})
        stat_val  = wb.add_format({'bold': True, 'bg_color': '#4472C4', 'font_color': '#FFFFFF',
                                   'align': 'center', 'border': 1, 'font_size': 13})

        # ══════════════════════════════════════════════════════
        #  SHEET 1 – Students List
        # ══════════════════════════════════════════════════════
        df_stu = pd.DataFrame(students_list)
        if df_stu.empty:
            df_stu = pd.DataFrame(columns=['moodle_id','roll_no','name','moodle_email','phone'])
        df_stu.columns = ['Moodle ID', 'Roll No', 'Name', 'Email', 'Phone']
        df_stu.to_excel(writer, sheet_name='Students List', index=False, startrow=1)
        ws1 = writer.sheets['Students List']
        ws1.write(0, 0, 'Student Master List', title_fmt)
        for c, w in enumerate([14, 12, 24, 30, 14]):
            ws1.set_column(c, c, w)
        for c in range(len(df_stu.columns)):
            ws1.write(1, c, df_stu.columns[c], hdr_fmt)

        # ══════════════════════════════════════════════════════
        #  SHEET 2 – Marks Analysis
        # ══════════════════════════════════════════════════════
        ws2 = wb.add_worksheet('Marks Analysis')
        writer.sheets['Marks Analysis'] = ws2
        row = 0

        # Title
        ws2.write(row, 0, 'Marks Analysis Report', title_fmt); row += 2

        # -- Avg per test table --
        ws2.write(row, 0, 'Average Score % per Test', hdr_fmt)
        ws2.write(row, 1, 'Avg %', hdr_fmt); row += 1
        for r in avg_test_data:
            ws2.write(row, 0, r['test_name'], cell_fmt)
            ws2.write(row, 1, float(r['avg_pct'] or 0), pct_fmt)
            row += 1
        row += 1

        # -- Top 10 students table --
        top10_start = row
        ws2.write(row, 0, 'Top 10 Students', title_fmt); row += 1
        hdrs = ['Rank', 'Moodle ID', 'Roll No', 'Name', 'Total Obtained', 'Total Max', 'Score %']
        for c, h in enumerate(hdrs):
            ws2.write(row, c, h, hdr_fmt)
            ws2.set_column(c, c, [6,14,12,22,14,10,10][c])
        row += 1
        for i, r in enumerate(marks['top10'], 1):
            fmt = green_fmt if float(r['avg_pct'] or 0) >= 40 else red_fmt
            ws2.write(row, 0, i, cell_fmt)
            ws2.write(row, 1, r['moodle_id'], cell_fmt)
            ws2.write(row, 2, r['roll_no'], cell_fmt)
            ws2.write(row, 3, r['name'], cell_fmt)
            ws2.write(row, 4, int(r['total_obtained'] or 0), cell_fmt)
            ws2.write(row, 5, int(r['total_max'] or 0), cell_fmt)
            ws2.write(row, 6, float(r['avg_pct'] or 0), fmt)
            row += 1
        row += 1

        # -- Pass/Fail table --
        ws2.write(row, 0, 'Pass vs Fail', title_fmt); row += 1
        ws2.write(row, 0, 'Status', hdr_fmt); ws2.write(row, 1, 'Count', hdr_fmt); row += 1
        ws2.write(row, 0, 'Pass', green_fmt); ws2.write(row, 1, int(pf['pass_count'] or 0), green_fmt); row += 1
        ws2.write(row, 0, 'Fail', red_fmt);  ws2.write(row, 1, int(pf['fail_count'] or 0), red_fmt);  row += 1
        row += 1

        # -- Distribution table --
        ws2.write(row, 0, 'Marks Distribution', title_fmt); row += 1
        for c, h in enumerate(dist_hdrs):
            ws2.write(row, c, h, hdr_fmt)
        row += 1
        for c, v in enumerate(dist_vals):
            ws2.write(row, c, v, cell_fmt)
        row += 2

        # -- Highest per test --
        ws2.write(row, 0, 'Highest Score % per Test', title_fmt); row += 1
        ws2.write(row, 0, 'Test Name', hdr_fmt); ws2.write(row, 1, 'Highest %', hdr_fmt); row += 1
        high_start = row
        for r in marks['highest_per_test']:
            ws2.write(row, 0, r['test_name'], cell_fmt)
            ws2.write(row, 1, float(r['highest_pct'] or 0), pct_fmt)
            row += 1

        # ══════════════════════════════════════════════════════
        #  SHEET 3 – Attendance Analysis
        # ══════════════════════════════════════════════════════
        ws3 = wb.add_worksheet('Attendance Analysis')
        writer.sheets['Attendance Analysis'] = ws3
        row = 0

        ws3.write(row, 0, 'Attendance Analysis Report', title_fmt); row += 2

        # All students attendance table
        ws3.write(row, 0, 'Student Attendance Summary', title_fmt); row += 1
        att_hdrs = ['Moodle ID', 'Roll No', 'Name', 'Attendance %']
        for c, h in enumerate(att_hdrs):
            ws3.write(row, c, h, hdr_fmt)
            ws3.set_column(c, c, [14,12,24,14][c])
        row += 1
        for r in att['all_attendance']:
            fmt = green_fmt if float(r['att_pct'] or 0) >= 75 else red_fmt
            ws3.write(row, 0, r['moodle_id'], cell_fmt)
            ws3.write(row, 1, r['roll_no'], cell_fmt)
            ws3.write(row, 2, r['name'], cell_fmt)
            ws3.write(row, 3, float(r['att_pct'] or 0), fmt)
            row += 1
        row += 1

        # Defaulters
        ws3.write(row, 0, 'Defaulters (Attendance < 75%)', title_fmt); row += 1
        for c, h in enumerate(att_hdrs):
            ws3.write(row, c, h, hdr_fmt)
        row += 1
        for r in att['defaulters']:
            ws3.write(row, 0, r['moodle_id'], cell_fmt)
            ws3.write(row, 1, r['roll_no'], cell_fmt)
            ws3.write(row, 2, r['name'], cell_fmt)
            ws3.write(row, 3, float(r['att_pct'] or 0), red_fmt)
            row += 1
        row += 1

        # Monthly trend
        ws3.write(row, 0, 'Monthly Attendance Trend', title_fmt); row += 1
        ws3.write(row, 0, 'Month', hdr_fmt)
        ws3.write(row, 1, 'Present', hdr_fmt)
        ws3.write(row, 2, 'Absent', hdr_fmt); row += 1
        monthly_start = row
        for r in att['monthly_trend']:
            ws3.write(row, 0, r['month'], cell_fmt)
            ws3.write(row, 1, int(r['present_cnt'] or 0), cell_fmt)
            ws3.write(row, 2, int(r['absent_cnt'] or 0), cell_fmt)
            row += 1
        monthly_end = row - 1

        # ══════════════════════════════════════════════════════
        #  SHEET 4 – Overall Class Analysis
        # ══════════════════════════════════════════════════════
        ws4 = wb.add_worksheet('Overall Analysis')
        writer.sheets['Overall Analysis'] = ws4

        ws4.write(0, 0, 'Overall Class Analysis', title_fmt)
        ws4.set_column(0, 0, 28); ws4.set_column(1, 1, 20)

        stats = [
            ('Total Students',        overall['total_students']),
            ('Average Score %',       f"{overall['avg_marks_pct']}%"),
            ('Average Attendance %',  f"{overall['avg_attendance']}%"),
            ('Pass Percentage',       f"{overall['pass_pct']}%"),
            ('Class Topper',          overall['topper']['name'] if overall['topper'] else 'N/A'),
            ('Topper Score %',        f"{overall['topper']['avg_pct']}%" if overall['topper'] else 'N/A'),
            ('Weak Students (< 40%)', len(overall['weak_students'])),
        ]
        for i, (lbl, val) in enumerate(stats, start=2):
            ws4.write(i, 0, lbl, stat_lbl)
            ws4.write(i, 1, str(val), stat_val)

        # Weak students table
        ws4.write(11, 0, 'Weak Students List (Score < 40%)', title_fmt)
        for c, h in enumerate(['Moodle ID', 'Roll No', 'Name', 'Avg Score %']):
            ws4.write(12, c, h, hdr_fmt)
        for i, r in enumerate(overall['weak_students']):
            ws4.write(13+i, 0, r['moodle_id'], cell_fmt)
            ws4.write(13+i, 1, r['roll_no'], cell_fmt)
            ws4.write(13+i, 2, r['name'], cell_fmt)
            ws4.write(13+i, 3, float(r['avg_pct'] or 0), red_fmt)

        # ══════════════════════════════════════════════════════
        #  SHEET 5 – Charts
        # ══════════════════════════════════════════════════════
        ws5 = wb.add_worksheet('Charts')
        writer.sheets['Charts'] = ws5
        ws5.write(0, 0, 'Analytics Charts', title_fmt)

        # Write data tables for charts on this sheet
        # -- Avg per test data (col A/B) --
        ws5.write(2, 0, 'Test', hdr_fmt); ws5.write(2, 1, 'Avg %', hdr_fmt)
        chart_data_start = 3
        for i, r in enumerate(avg_test_data):
            ws5.write(chart_data_start+i, 0, r['test_name'], cell_fmt)
            ws5.write(chart_data_start+i, 1, float(r['avg_pct'] or 0), pct_fmt)
        chart_data_end = chart_data_start + len(avg_test_data) - 1

        # Bar chart – avg score per test
        if avg_test_data:
            bar = wb.add_chart({'type': 'column'})
            bar.add_series({
                'name': 'Avg Score %',
                'categories': ['Charts', chart_data_start, 0, chart_data_end, 0],
                'values':     ['Charts', chart_data_start, 1, chart_data_end, 1],
                'fill': {'color': '#4472C4'}, 'gap': 60,
            })
            bar.set_title({'name': 'Average Score % per Test'})
            bar.set_x_axis({'name': 'Test'}); bar.set_y_axis({'name': '%', 'min': 0, 'max': 100})
            bar.set_size({'width': 480, 'height': 300}); bar.set_style(10)
            ws5.insert_chart('D2', bar)

        # -- Pass/Fail pie data (col A/B, below test data) --
        pie_start = chart_data_end + 3
        ws5.write(pie_start,   0, 'Status', hdr_fmt); ws5.write(pie_start,   1, 'Count', hdr_fmt)
        ws5.write(pie_start+1, 0, 'Pass',   cell_fmt); ws5.write(pie_start+1, 1, int(pf['pass_count'] or 0), cell_fmt)
        ws5.write(pie_start+2, 0, 'Fail',   cell_fmt); ws5.write(pie_start+2, 1, int(pf['fail_count'] or 0), cell_fmt)

        pie = wb.add_chart({'type': 'pie'})
        pie.add_series({
            'name': 'Pass vs Fail',
            'categories': ['Charts', pie_start+1, 0, pie_start+2, 0],
            'values':     ['Charts', pie_start+1, 1, pie_start+2, 1],
            'points': [{'fill': {'color': '#70AD47'}}, {'fill': {'color': '#FF0000'}}],
        })
        pie.set_title({'name': 'Pass vs Fail Ratio'})
        pie.set_style(10); pie.set_size({'width': 380, 'height': 280})
        ws5.insert_chart('D22', pie)

        # -- Distribution bar (col A/B) --
        dist_start = pie_start + 5
        ws5.write(dist_start, 0, 'Range', hdr_fmt); ws5.write(dist_start, 1, 'Students', hdr_fmt)
        for i, (lbl, val) in enumerate(zip(dist_hdrs, dist_vals)):
            ws5.write(dist_start+1+i, 0, lbl, cell_fmt)
            ws5.write(dist_start+1+i, 1, val, cell_fmt)

        dist_chart = wb.add_chart({'type': 'bar'})
        dist_chart.add_series({
            'name': 'Students',
            'categories': ['Charts', dist_start+1, 0, dist_start+4, 0],
            'values':     ['Charts', dist_start+1, 1, dist_start+4, 1],
            'fill': {'color': '#ED7D31'}, 'gap': 50,
        })
        dist_chart.set_title({'name': 'Marks Distribution'})
        dist_chart.set_size({'width': 420, 'height': 280}); dist_chart.set_style(10)
        ws5.insert_chart('D42', dist_chart)

        # -- Monthly attendance line chart --
        if att['monthly_trend']:
            line = wb.add_chart({'type': 'line'})
            line.add_series({
                'name': 'Present',
                'categories': ['Attendance Analysis', monthly_start, 0, monthly_end, 0],
                'values':     ['Attendance Analysis', monthly_start, 1, monthly_end, 1],
                'line': {'color': '#70AD47', 'width': 2.5},
            })
            line.add_series({
                'name': 'Absent',
                'categories': ['Attendance Analysis', monthly_start, 0, monthly_end, 0],
                'values':     ['Attendance Analysis', monthly_start, 2, monthly_end, 2],
                'line': {'color': '#FF0000', 'width': 2.5},
            })
            line.set_title({'name': 'Monthly Attendance Trend'})
            line.set_x_axis({'name': 'Month'}); line.set_y_axis({'name': 'Count'})
            line.set_size({'width': 500, 'height': 300}); line.set_style(10)
            ws5.insert_chart('D62', line)

        ws5.set_column(0, 1, 16)

    output.seek(0)
    return output
