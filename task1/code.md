Here is a complete system design, algorithm, Mermaid flowchart, and Python implementation for the **University Scholarship Allocation System**.

---

## 1. Problem Statement

A university wants to automate its annual merit-based and need-based scholarship allocation process. The system must process a list of applicant profiles and determine scholarship recipients based on strict eligibility criteria, merit ranking, and predefined tie-breaking rules.

### **Eligibility Criteria:**

1. **Aggregate Marks:** Must be greater than or equal to a specified minimum threshold (e.g., 75.0%).
2. **Subject-wise Minimum Scores:** Must meet or exceed a minimum passing score in every individual subject (e.g., $\ge 60$).
3. **Attendance:** Must have a minimum attendance percentage (e.g., $\ge 85.0\%$).
4. **Income Criteria:** Annual family income must be below or equal to a specified ceiling (e.g., ₹6,00,000) to ensure need-based support.

### **Ranking & Tie-Breaking Rules:**

Eligible students are ranked using a multi-level sorting strategy:

1. **Primary Key:** Aggregate Marks (Descending order — highest marks first).
2. **Secondary Key:** Attendance Percentage (Descending order).
3. **Tertiary Key:** Annual Family Income (Ascending order — lower income prioritized in ties).
4. **Quaternary Key:** Student ID (Ascending order for deterministic ordering).

---

## 2. Algorithm

1. **Initialize Inputs:** Define scholarship constraints (minimum aggregate, subject minimums, minimum attendance, max income, and total available scholarship slots).
2. **Filter Applicants (Eligibility Check):**
* For each student, check if:
* `aggregate_marks >= min_aggregate`
* All `subject_scores >= min_subject_score`
* `attendance >= min_attendance`
* `annual_income <= max_income`


* If all conditions are met, mark the student as **Eligible**; otherwise, **Rejected/Ineligible**.


3. **Sort Eligible Students:** Sort the list of eligible students using the tie-breaking tuple: `(-aggregate_marks, -attendance, annual_income, student_id)`.
4. **Allocate Scholarships:**
* Iterate through the sorted eligible list.
* Assign scholarships up to the maximum available quota.
* Remaining eligible students are placed on a **Waitlist**.


5. **Output Results:** Display the allocated scholars, waitlisted candidates, and rejected applicants with reasons.

---

## 3. Flowchart (Mermaid)

```mermaid
graph TD
    Start([Start]) --> Input[Input Student Records & Criteria]
    Input --> LoopStart{More Students?}
    
    LoopStart -- Yes --> CheckElig{Check Eligibility:<br/>- Aggregate >= Min?<br/>- All Subjects >= Min?<br/>- Attendance >= Min?<br/>- Income <= Max?}
    
    CheckElig -- No --> MarkReject[Mark as Ineligible/Rejected] --> LoopStart
    CheckElig -- Yes --> MarkElig[Mark as Eligible] --> LoopStart
    
    LoopStart -- No --> SortElig[Sort Eligible Students<br/>1. Desc Aggregate<br/>2. Desc Attendance<br/>3. Asc Income<br/>4. Asc ID]
    
    SortElig --> Alloc[Allocate Scholarships up to Quota Limit]
    Alloc --> Output[Generate Report:<br/>- Awarded Scholars<br/>- Waitlist<br/>- Rejected]
    Output --> End([End])

```

---


## 5. Sample Input & Output

### **Sample Input Configuration**

* **Minimum Aggregate:** $75.0\%$
* **Subject Minimum:** $60$ marks
* **Minimum Attendance:** $85.0\%$
* **Maximum Family Income:** ₹6,00,000
* **Total Scholarship Slots:** $3$

*(See the `applicants` list in the Python code above for student data profiles, including edge cases like failing income thresholds, failing subject minimums, and tie-breaking scenarios).*

### **Sample Output**

```text
=== SCHOLARSHIP ALLOCATION RESULTS ===

Total Available Slots: 3

--- AWARDED SCHOLARS ---
1. [S104] Diana Prince | Marks: 88.5% | Attendance: 96.0% | Income: ₹400000
2. [S101] Alice Smith | Marks: 88.5% | Attendance: 92.0% | Income: ₹450000
3. [S105] Evan Wright | Marks: 82.0% | Attendance: 90.0% | Income: ₹250000

--- WAITLISTED STUDENTS ---
(None, all eligible candidates accommodated within slots)

--- REJECTED STUDENTS ---
- [S102] Bob Jones: Annual income 700000 exceeds limit 600000
- [S103] Charlie Brown: One or more subject scores below minimum 60

```
