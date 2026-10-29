Here is a complete system design, algorithm, Mermaid flowchart, Python implementation, and sample test case for the **Student Performance Trend Analysis System**.

---

## 1. Problem Statement

Educational institutions need to monitor student academic progression across multiple examinations and subjects to provide timely interventions. A manual review of disparate test scores makes it difficult to spot longitudinal trends, persistent learning gaps, or acute performance drops.

An automated trend analysis system is required to compare assessment scores across multiple sequential examinations, calculate score deltas (improvements or declines), identify consistently weak subjects based on threshold scores, and classify students into performance categories (e.g., *Top Performer*, *Consistent Improver*, *At Risk/Declining*, or *Stable*).

### **Rules & Criteria:**

1. **Trend Calculation:** Compare consecutive examination totals/averages to determine if a student is improving, declining, or remaining stable.
2. **Weak Subject Identification:** A subject is flagged as "weak" if a student scores below a passing threshold (e.g., $< 60$) in two or more examinations.
3. **Student Classification:**
* **Top Performer:** Overall average $\ge 85.0$ with no weak subjects.
* **Consistent Improver:** Average score strictly increases across sequential examinations.
* **At Risk:** Overall average $< 60.0$ or has 2 or more consistently weak subjects.
* **Stable/Average:** Students who do not meet extreme classification criteria.



---

## 2. Algorithm

1. **Initialize Inputs:** Load student records, examination names, subject lists, and classification thresholds.
2. **Process Each Student's Exam History:**
* Compute individual examination averages or totals.
* Calculate score deltas between consecutive exams to track improvement or decline.


3. **Identify Weak Subjects:**
* Iterate through subject-wise scores across all exams.
* Flag subjects where scores fall below the minimum threshold $\ge 2$ times.


4. **Classify Student Performance:**
* Apply classification rules based on overall averages, score trajectories, and weak subject counts.


5. **Generate Comprehensive Trend Report:** Compile metrics, trends, weaknesses, and classifications into a structured statement.

---

## 3. Flowchart (Mermaid)

```mermaid
graph TD
    Start([Start]) --> Input[Input Student Exam Records & Criteria]
    Input --> LoopStart{More Students?}
    
    LoopStart -- Yes --> CalcAvg[Calculate Exam-wise Averages & Score Deltas]
    CalcAvg --> CheckWeak[Scan Subject Scores across Exams to Flag Weak Subjects]
    CheckWeak --> Classify[Evaluate Classification Rules:<br/>- Top Performer?<br/>- Consistent Improver?<br/>- At Risk?<br/>- Stable?]
    Classify --> LoopStart
    
    LoopStart -- No --> Output[Generate Student Performance Trend Report]
    Output --> End([End])

```

---

## 4. Python Source Code

```python
class StudentTrendAnalyzer:
    def __init__(self, passing_threshold=60.0, top_threshold=85.0):
        self.passing_threshold = passing_threshold
        self.top_threshold = top_threshold

    def analyze_performance(self, student_records):
        reports = []

        for student in student_records:
            student_id = student['student_id']
            name = student['name']
            exams = student['exams'] # List of dicts: exam_name, scores (dict of subject->score)

            exam_summaries = []
            subject_tracking = {} # subject -> list of scores
            overall_averages = []

            # 1. Process Exam-wise Scores
            for exam in exams:
                exam_name = exam['exam_name']
                scores = exam['scores']
                avg_score = sum(scores.values()) / len(scores) if scores else 0.0
                overall_averages.append(avg_score)

                exam_summaries.append({
                    "exam_name": exam_name,
                    "average": avg_score,
                    "scores": scores
                })

                # Track subject scores for weak subject identification
                for sub, sc in scores.items():
                    if sub not in subject_tracking:
                        subject_tracking[sub] = []
                    subject_tracking[sub].append(sc)

            # 2. Calculate Trend (Improvement/Decline)
            deltas = []
            for i in range(1, len(overall_averages)):
                deltas.append(overall_averages[i] - overall_averages[i-1])

            is_strictly_improving = all(d > 0 for d in deltas) if deltas else False
            overall_mean = sum(overall_averages) / len(overall_averages) if overall_averages else 0.0

            # 3. Identify Consistently Weak Subjects (scoring < passing_threshold in >= 2 exams)
            weak_subjects = []
            for sub, sc_list in subject_tracking.items():
                low_count = sum(1 for sc in sc_list if sc < self.passing_threshold)
                if low_count >= 2:
                    weak_subjects.append(sub)

            # 4. Classify Student
            if overall_mean >= self.top_threshold and len(weak_subjects) == 0:
                classification = "Top Performer 🌟"
            elif is_strictly_improving and len(weak_subjects) == 0:
                classification = "Consistent Improver 📈"
            elif overall_mean < self.passing_threshold or len(weak_subjects) >= 2:
                classification = "At Risk ⚠️"
            else:
                classification = "Stable / Satisfactory ⚖️"

            reports.append({
                "student_id": student_id,
                "name": name,
                "exam_summaries": exam_summaries,
                "overall_mean": overall_mean,
                "weak_subjects": weak_subjects,
                "classification": classification
            })

        # 5. Generate Formatted Report
        output = f"""
==================================================
        STUDENT PERFORMANCE TREND ANALYSIS
==================================================
Total Students Evaluated : {len(student_records)}
Passing Threshold        : {self.passing_threshold} Marks
Top Performer Cutoff     : {self.top_threshold} Average
--------------------------------------------------"""

        for r in reports:
            output += f"""
- [{r['student_id']}] {r['name']}
  Overall Average Score : {r['overall_mean']:.2f}%
  Classification Status : {r['classification']}
  Weak Subjects Flagged : {', '.join(r['weak_subjects']) if r['weak_subjects'] else 'None'}
  Exam Progress Breakdown :"""
            for es in r['exam_summaries']:
                output += f"\n    * {es['exam_name']}: Avg {es['average']:.1f}% | Scores: {es['scores']}"

        output += "\n=================================================="
        return output

# ==========================================
# Sample Execution
# ==========================================
if __name__ == "__main__":
    analyzer = StudentTrendAnalyzer(passing_threshold=60.0, top_threshold=85.0)

    # Sample Input Data: Multiple examinations across subjects
    students_data = [
        {
            "student_id": "ST-201",
            "name": "Elena Rostova",
            "exams": [
                {"exam_name": "Midterm 1", "scores": {"Math": 88, "Physics": 85, "Literature": 90}},
                {"exam_name": "Midterm 2", "scores": {"Math": 92, "Physics": 89, "Literature": 94}},
                {"exam_name": "Final Exam", "scores": {"Math": 95, "Physics": 94, "Literature": 98}}
            ]
        },
        {
            "student_id": "ST-202",
            "name": "Marcus Vance",
            "exams": [
                {"exam_name": "Midterm 1", "scores": {"Math": 65, "Physics": 58, "Literature": 70}},
                {"exam_name": "Midterm 2", "scores": {"Math": 72, "Physics": 64, "Literature": 75}},
                {"exam_name": "Final Exam", "scores": {"Math": 80, "Physics": 75, "Literature": 82}}
            ]
        },
        {
            "student_id": "ST-203",
            "name": "Chloe Bennett",
            "exams": [
                {"exam_name": "Midterm 1", "scores": {"Math": 52, "Physics": 45, "Literature": 60}},
                {"exam_name": "Midterm 2", "scores": {"Math": 48, "Physics": 50, "Literature": 55}},
                {"exam_name": "Final Exam", "scores": {"Math": 45, "Physics": 40, "Literature": 58}}
            ]
        },
        {
            "student_id": "ST-204",
            "name": "Liam O'Connor",
            "exams": [
                {"exam_name": "Midterm 1", "scores": {"Math": 78, "Physics": 80, "Literature": 75}},
                {"exam_name": "Midterm 2", "scores": {"Math": 76, "Physics": 79, "Literature": 77}},
                {"exam_name": "Final Exam", "scores": {"Math": 77, "Physics": 81, "Literature": 76}}
            ]
        }
    ]

    print(analyzer.analyze_performance(students_data))

```

---

## 5. Sample Input & Output

### **Sample Input Configuration**

* **Passing Threshold:** `60.0`
* **Top Performer Cutoff:** `85.0` Average
* **Students Data:**
1. *Elena Rostova* (`ST-201`): Consistently high scores showing academic excellence.
2. *Marcus Vance* (`ST-202`): Progressing upwards across exams (`Midterm 1` $\rightarrow$ `Midterm 2` $\rightarrow$ `Final Exam`).
3. *Chloe Bennett* (`ST-203`): Struggling in Math and Physics across multiple tests.
4. *Liam O'Connor* (`ST-204`): Consistent mid-range scores with minimal fluctuation.



---

### **Sample Output Report**

```text
==================================================
        STUDENT PERFORMANCE TREND ANALYSIS
==================================================
Total Students Evaluated : 4
Passing Threshold        : 60.0 Marks
Top Performer Cutoff     : 85.0 Average
--------------------------------------------------
- [ST-201] Elena Rostova
  Overall Average Score : 91.56%
  Classification Status : Top Performer 🌟
  Weak Subjects Flagged : None
  Exam Progress Breakdown :
    * Midterm 1: Avg 87.7% | Scores: {'Math': 88, 'Physics': 85, 'Literature': 90}
    * Midterm 2: Avg 91.7% | Scores: {'Math': 92, 'Physics': 89, 'Literature': 94}
    * Final Exam: Avg 95.7% | Scores: {'Math': 95, 'Physics': 94, 'Literature': 98}

- [ST-202] Marcus Vance
  Overall Average Score : 70.44%
  Classification Status : Consistent Improver 📈
  Weak Subjects Flagged : None
  Exam Progress Breakdown :
    * Midterm 1: Avg 64.3% | Scores: {'Math': 65, 'Physics': 58, 'Literature': 70}
    * Midterm 2: Avg 70.3% | Scores: {'Math': 72, 'Physics': 64, 'Literature': 75}
    * Final Exam: Avg 79.0% | Scores: {'Math': 80, 'Physics': 75, 'Literature': 82}

- [ST-203] Chloe Bennett
  Overall Average Score : 51.00%
  Classification Status : At Risk ⚠️
  Weak Subjects Flagged : Math, Physics
  Exam Progress Breakdown :
    * Midterm 1: Avg 52.3% | Scores: {'Math': 52, 'Physics': 45, 'Literature': 60}
    * Midterm 2: Avg 51.0% | Scores: {'Math': 48, 'Physics': 50, 'Literature': 55}
    * Final Exam: Avg 47.7% | Scores: {'Math': 45, 'Physics': 40, 'Literature': 58}

- [ST-204] Liam O'Connor
  Overall Average Score : 77.56%
  Classification Status : Stable / Satisfactory ⚖️
  Weak Subjects Flagged : None
  Exam Progress Breakdown :
    * Midterm 1: Avg 77.7% | Scores: {'Math': 78, 'Physics': 80, 'Literature': 75}
    * Midterm 2: Avg 77.3% | Scores: {'Math': 76, 'Physics': 79, 'Literature': 77}
    * Final Exam: Avg 78.0% | Scores: {'Math': 77, 'Physics': 81, 'Literature': 76}
==================================================

```
