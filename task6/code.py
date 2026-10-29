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

                for sub, sc in scores.items():
                    if sub not in subject_tracking:
                        subject_tracking[sub] = []
                    subject_tracking[sub].append(sc)

            deltas = []
            for i in range(1, len(overall_averages)):
                deltas.append(overall_averages[i] - overall_averages[i-1])

            is_strictly_improving = all(d > 0 for d in deltas) if deltas else False
            overall_mean = sum(overall_averages) / len(overall_averages) if overall_averages else 0.0

            weak_subjects = []
            for sub, sc_list in subject_tracking.items():
                low_count = sum(1 for sc in sc_list if sc < self.passing_threshold)
                if low_count >= 2:
                    weak_subjects.append(sub)

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


if __name__ == "__main__":
    analyzer = StudentTrendAnalyzer(passing_threshold=60.0, top_threshold=85.0)

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
