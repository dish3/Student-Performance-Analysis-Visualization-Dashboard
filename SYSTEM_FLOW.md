# System Flow Diagram

## User Authentication Flow

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Login Page     │
│  (login.html)   │
└──────┬──────────┘
       │
       ▼
┌─────────────────────────────┐
│  Check Credentials          │
│  - Query faculty table      │
│  - Verify hashed password   │
└──────┬──────────────────────┘
       │
       ├─── Admin ────────────────┐
       │                          │
       ▼                          ▼
┌──────────────────┐    ┌──────────────────┐
│ Admin Dashboard  │    │ Faculty Dashboard│
└──────────────────┘    └──────────────────┘
```

## Admin Test Creation Flow

```
Step 1: Create Test
┌─────────────────────────┐
│  Admin clicks           │
│  "Create Test"          │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Enter Test Name        │
│  (e.g., "Unit Test 1")  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Save to tests table    │
│  Get test_id            │
└───────────┬─────────────┘
            │
            ▼

Step 2: Add Questions
┌─────────────────────────┐
│  Enter number of        │
│  questions (e.g., 10)   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Show form with         │
│  10 input fields        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Enter max marks for    │
│  each question:         │
│  Q1: 5 marks            │
│  Q2: 10 marks           │
│  Q3: 5 marks            │
│  ... etc                │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Save to                │
│  test_questions table   │
│  (10 rows)              │
└─────────────────────────┘
```

## Faculty Marks Entry Flow

```
Step 1: Select Test & Student
┌─────────────────────────┐
│  Faculty clicks         │
│  "Enter Marks"          │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Show dropdowns:        │
│  - Select Test          │
│  - Select Student       │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Faculty selects:       │
│  Test: "Unit Test 1"    │
│  Student: "John Doe"    │
└───────────┬─────────────┘
            │
            ▼

Step 2: Enter Marks
┌─────────────────────────┐
│  System loads:          │
│  - All questions        │
│  - Max marks per Q      │
│  - Existing marks or 0  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Show marks form:       │
│  Q1: [3] / 5            │
│  Q2: [8] / 10           │
│  Q3: [4] / 5            │
│  ... etc                │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Faculty edits marks    │
│  and clicks Submit      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Save to                │
│  student_test_marks     │
│  (one row per question) │
└─────────────────────────┘
```

## View Marks Flow

```
┌─────────────────────────┐
│  Faculty clicks         │
│  "View Marks"           │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Query database:        │
│  - Join students        │
│  - Join tests           │
│  - Sum marks            │
│  - Calculate %          │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Show summary table:    │
│  Student | Test | Total │
│  John    | UT1  | 15/20 │
│  Jane    | UT1  | 18/20 │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Click "View Details"   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Show question-wise:    │
│  Q1: 3/5                │
│  Q2: 8/10               │
│  Q3: 4/5                │
│  Total: 15/20 (75%)     │
└─────────────────────────┘
```

## Database Relationships

```
┌──────────────┐
│   students   │
│──────────────│
│ id (PK)      │◄─────┐
│ name         │      │
│ email        │      │
│ phone        │      │
└──────────────┘      │
                      │
┌──────────────┐      │
│   faculty    │      │
│──────────────│      │
│ faculty_id   │      │
│ username     │      │
│ password     │      │
│ role         │      │
└──────────────┘      │
                      │
┌──────────────┐      │
│    tests     │      │
│──────────────│      │
│ test_id (PK) │◄─┐   │
│ test_name    │  │   │
└──────────────┘  │   │
                  │   │
┌──────────────────┐ │   │
│ test_questions   │ │   │
│──────────────────│ │   │
│ question_id (PK) │◄┼───┼─┐
│ test_id (FK)     │─┘   │ │
│ question_number  │     │ │
│ max_marks        │     │ │
└──────────────────┘     │ │
                         │ │
┌────────────────────────┐│ │
│ student_test_marks     ││ │
│────────────────────────││ │
│ id (PK)                ││ │
│ student_id (FK)        │┼─┘
│ test_id (FK)           │┼───┘
│ question_id (FK)       │┼───┘
│ obtained_marks         ││
└────────────────────────┘│
```

## Data Flow Example

### Example: Creating a test and entering marks

```
1. Admin creates "Unit Test 1"
   ↓
   tests table: test_id=1, test_name="Unit Test 1"

2. Admin adds 3 questions
   ↓
   test_questions table:
   - question_id=1, test_id=1, question_number=1, max_marks=5
   - question_id=2, test_id=1, question_number=2, max_marks=10
   - question_id=3, test_id=1, question_number=3, max_marks=5

3. Faculty enters marks for student_id=1
   ↓
   student_test_marks table:
   - id=1, student_id=1, test_id=1, question_id=1, obtained_marks=3
   - id=2, student_id=1, test_id=1, question_id=2, obtained_marks=8
   - id=3, student_id=1, test_id=1, question_id=3, obtained_marks=4

4. View marks calculates:
   Total obtained: 3 + 8 + 4 = 15
   Total max: 5 + 10 + 5 = 20
   Percentage: (15/20) * 100 = 75%
```

## Security Flow

```
┌─────────────────┐
│  User enters    │
│  password       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Werkzeug       │
│  hashes         │
│  password       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Compare with   │
│  stored hash    │
│  in database    │
└────────┬────────┘
         │
         ├─── Match ────► Create session
         │
         └─── No Match ─► Show error
```

## Session Management

```
┌─────────────────┐
│  Login Success  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Store in session:      │
│  - logged_in = True     │
│  - username = "admin"   │
│  - faculty_id = 1       │
│  - role = "admin"       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Every request checks:  │
│  - Is logged_in?        │
│  - What role?           │
│  - Redirect if needed   │
└─────────────────────────┘
```

## Complete User Journey

```
START
  │
  ▼
Login ──► Check Role
  │           │
  │           ├─── Admin ───► Admin Dashboard
  │           │                    │
  │           │                    ├─► Create Test
  │           │                    ├─► Add Students
  │           │                    └─► Add Faculty
  │           │
  │           └─── Faculty ─► Faculty Dashboard
  │                               │
  │                               ├─► Enter Marks
  │                               └─► View Marks
  │
  ▼
Logout ──► Clear Session ──► Redirect to Login
```
