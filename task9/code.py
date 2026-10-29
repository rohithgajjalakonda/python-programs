class MarksMatrixAnalyzer:
    def __init__(self, low_threshold=65.0):
        self.low_threshold = low_threshold

    def analyze_matrix(self, student_names, subjects, marks_matrix):
        num_students = len(student_names)
        num_subjects = len(subjects)
        
        student_stats = []
        subject_totals = [0.0] * num_subjects
        subject_max = [float('-inf')] * num_subjects
        subject_min = [float('inf')] * num_subjects

       
        for i in range(num_students):
            name = student_names[i]
            row_marks = marks_matrix[i]
            total_marks = sum(row_marks)
            avg_score = total_marks / num_subjects

            student_stats.append({
                "name": name,
                "marks": row_marks,
                "total": total_marks,
                "average": avg_score
            })

           
            for j in range(num_subjects):
                score = row_marks[j]
                subject_totals[j] += score
                if score > subject_max[j]:
                    subject_max[j] = score
                if score < subject_min[j]:
                    subject_min[j] = score

        
        subject_stats = []
        low_performing_subjects = []

        for j in range(num_subjects):
            sub_name = subjects[j]
            sub_avg = subject_totals[j] / num_students
            is_low = sub_avg < self.low_threshold

            if is_low:
                low_performing_subjects.append(sub_name)

            subject_stats.append({
                "subject": sub_name,
                "average": sub_avg,
                "max": subject_max[j],
                "min": subject_min[j],
                "is_low": is_low
            })

       
        top_student = max(student_stats, key=lambda x: x['total'])

      
        report = f"""
==================================================
           STUDENT MARKS MATRIX ANALYSIS
==================================================
Total Students Evaluated : {num_students}
Total Subjects Assessed  : {num_subjects}
Low Performance Threshold: {self.low_threshold}%
--------------------------------------------------
STUDENT PERFORMANCE SUMMARY (ROW-WISE)
--------------------------------------------------"""

        for s in student_stats:
            report += f"\n- {s['name']:<15} | Total: {s['total']:<6.1f} | Average: {s['average']:.2f}% | Marks: {s['marks']}"

        report += f"""
--------------------------------------------------
SUBJECT PERFORMANCE SUMMARY (COLUMN-WISE)
--------------------------------------------------"""

        for sub in subject_stats:
            status_tag = " [LOW PERFORMANCE ⚠️]" if sub['is_low'] else " [Healthy ✅]"
            report += f"\n- {sub['subject']:<12} | Avg: {sub['average']:<5.1f}% | Max: {sub['max']:<3} | Min: {sub['min']:<3}{status_tag}"

        report += f"""
--------------------------------------------------
COHORT HIGHLIGHTS
--------------------------------------------------
Top Performing Student : {top_student['name']} with {top_student['total']} total marks ({top_student['average']:.2f}%) 🌟
Flagged Weak Subjects  : {', '.join(low_performing_subjects) if low_performing_subjects else 'None'}
==================================================
"""
        return report


if __name__ == "__main__":
    analyzer = MarksMatrixAnalyzer(low_threshold=70.0)

  
    subjects_list = ["Mathematics", "Physics", "Chemistry", "Computer Science"]
    students_list = ["Alice Smith", "Bob Jones", "Charlie Brown", "Diana Prince", "Evan Wright"]
    
  
    marks_matrix_data = [
        [88, 92, 90, 95],  # Alice
        [65, 58, 62, 70],  # Bob
        [78, 85, 80, 82],  # Charlie
        [95, 94, 96, 98],  # Diana
        [72, 68, 65, 74]   # Evan
    ]

    print(analyzer.analyze_matrix(students_list, subjects_list, marks_matrix_data))
