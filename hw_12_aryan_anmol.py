"""Web Page for the student repository using flask"""
from typing import List,Tuple,Dict
import sqlite3
from flask import Flask, render_template
app: Flask = Flask(__name__)
database_file: str = r"C:\Users\aryan\Documents\SSW 810\12th Assingment\HW11_db"
@app.route('/12TH ASSINGMENT')
def completed_courses():
    """Get Tables from data base and link it to """
    try:
        db: sqlite3.Connection = sqlite3.connect(database_file)
    except sqlite3.OperationalError as e:
        print("Database not found")
    else:
        query: str = """select students.Name as Student_Name, students.CWID, grades.Course, grades.Grade, instructors.Name as Instructor_Name \
                    from ((students inner join grades on students.CWID = grades.StudentCWID) \
                    inner join instructors on grades.InstructorCWID = instructors.CWID) order by Student_Name ASC"""
        data: Dict[str, str] = \
            [{"name": name, "cwid": cwid, "major": major, "grade": grade, "instructor": instructor} 
                for name, cwid, major, grade, instructor in db.execute(query)]

        db.close()

    return render_template(
        'students_summary.html',
        title="Stevens Repository",
        table_title="Students courses and grade",
        students=data)
app.run(debug=True)