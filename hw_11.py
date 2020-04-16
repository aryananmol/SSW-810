"""Student repository with database"""
import os
from collections import defaultdict
from prettytable import PrettyTable
from typing import DefaultDict, Dict, Tuple, List, Iterator, Set
import sqlite3

'''reading files and printing them in a table format'''

class Student:
    """ Store everything about a single student """
    pt_hdr: List[str] = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives', 'GPA']
    grade_point: Dict[str,float] = {'A' : 4.0, 'A-' : 3.75, 'B+' : 3.25, 'B' : 3.0, 'B-' : 2.75, 'C+' : 2.25, \
                'C' : 2.0, 'C-' : 0, 'D+' : 0, 'D' : 0,'D-' : 0, 'F' : 0}

    def __init__(self, cwid: str, name: str, major: str, required: List[str], electives: List[str]) -> None:
        """ store every info about a student """
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._course: Dict[str, str] = dict()
        self._remaining_required: List[str] = required
        self._remaining_electives: List[str] = electives
        self._gpa: float = 0.0 

    def store_course_grade(self, course: str, grade:str) -> None:
        """ store grade with respect to course student has taken """
        if grade in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']:
            self._course[course] = grade
        elif grade in ['C-', 'D+', 'D', 'D-', 'F']:
            print(f'Student with CWID {self._cwid} has failed this course.')
        else:
            print(f'Student with CWID {self._cwid} has no record with this course.')

        if len(self._course.values()) > 0 :
            self._gpa = round(sum([Student.grade_point[grade] for grade in self._course.values()])/len(self._course.values()), 2)

    def student_info(self) -> Tuple[str, str, List[str], List[str], List[str], float]:
        """ return information needed for student pretty table """
        
        remaining_req: Set[str] = set(self._remaining_required) - set(self._course)
        remaining_elec: Set[str] = set(self._remaining_electives) - set(self._course)
        if len(remaining_elec) < len(self._remaining_electives):
            remaining_elec = []
            
        return self._cwid, self._name, self._major, sorted(self._course.keys()), sorted(remaining_req), sorted(remaining_elec), self._gpa

class Instructor:
    """Store instructor inforamtion"""
    pt_hdr: List[str] = ['CWID', 'Name', 'Dept', 'Course', 'Students']

    def __init__(self, cwid: str, name:str, major:str ) -> None:
        """ store every info about a instructor """
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: DefaultDict[str, int] = defaultdict(int)
    
    def store_course_students(self, course: str) -> None:
        """ counting how many students are in a particular course instructor is taking """
        self._courses[course] += 1
        
    def instructor_info(self) -> Iterator[Tuple[str, str, str, str, int]]:
        """ return information needed for instructor pretty table """
        # list_inst: list = list()
        for course, student_number in self._courses.items():
            # list_inst.append([self._cwid, self._name, self._major, course, student_number])
            yield self._cwid, self._name, self._major, course, student_number
        # return list_inst

class Major:
    """Store major information"""
    pt_hdr: List[str] = ['Major', 'Required Courses', 'Electives']

    def __init__(self, major: str) -> None:
        """ store every info about a major """
        self._major: str = major
        self._required: Set[str] = set()
        self._electives: Set[str] = set()

    def add_course(self, course_type: str, course: str) -> List:
        """ add course to their respective category """
        if course_type.upper() == 'R':
            self._required.add(course)
        elif course_type.upper() == 'E':
            self._electives.add(course)
        else:
            print(f"Unknown type {course_type} found.")

    def get_required(self):
        return self._required

    def get_electives(self):
        return self._electives

    def major_info(self) -> Tuple[str, str, str]:
        """ return information needed for instructor pretty table """
        return self._major, sorted(self._required), sorted(self._electives)

class University:
        """ Repository to store students instructors for university and print pretty table """

        def __init__(self, path: str)->None:
            """ store students, instructors and pretty table """
            self._path = path
            self._students: Dict[str, Student] = dict()
            self._instructors: Dict[str, Instructor] = dict()
            self._majors: Dict[str, Major] = dict()
            self._read_majors()
            self._read_students()
            self._read_instructors()
            self._read_grades()
            
        def _read_students(self) -> None:
            """ read student file and assigning values to dictionary """
            try:
                directory: str = os.path.join(self._path, 'students.txt')
            except(FileNotFoundError) as e:
                print(e)
            else:
                for cwid, name, major in file_reader(directory, 3, sep = '\t', header = True):
                    self._students[cwid] = Student(cwid, name, major, self._majors[major].get_required(), self._majors[major].get_electives())
                    # return self._students
                    # print(self._students)
            
        def _read_instructors(self) -> None:
            """ read instructor file and assigning values to dictionary """
            try:
                directory: str = os.path.join(self._path, 'instructors.txt')
            except(FileNotFoundError) as e:
                print(e)
            else:
                for cwid, name, major in file_reader(directory, 3, sep = '\t', header = True):
                    self._instructors[cwid] = Instructor(cwid, name, major)
                    # print(self._instructors)
                    # return self._instructors

        def _read_grades(self) -> None:
            """ read grades file and assigning values to dictionary """
            try:
                directory: str = os.path.join(self._path, 'grades.txt')
            except(FileNotFoundError) as e:
                print(e)
            else:
                for student_cwid, course, grade, instructor_cwid in file_reader(directory, 4, sep = '\t', header = True):
                    if student_cwid in self._students.keys():
                        self._students[student_cwid].store_course_grade(course, grade)
                        # return grade
                    else:
                        raise ValueError(f"student with id: {student_cwid} is not matched with any data")

                    if instructor_cwid in self._instructors.keys():
                        self._instructors[instructor_cwid].store_course_students(course)
                        # return self._instructors
                    else:
                        raise ValueError(f"professor with id: {instructor_cwid} is not matched with any data")

        def _read_majors(self) -> None:
            """ read grades file and assigning values to dictionary """
            try:
                directory: str = os.path.join(self._path, 'majors.txt')
            except(FileNotFoundError) as e:
                print(e)
            else:
                for major, r_e, course in file_reader(directory, 3, sep = '\t', header = True):
                    if major not in self._majors.keys():
                        # self._majors[major] = Major(major, r_e, course)
                        self._majors[major] = Major(major)
                    self._majors[major].add_course(r_e, course)
                    # print(self._majors)

        def major_prettytable(self):
            """Sends the major data to the pretty table and prints it"""
            pretty_table3: PrettyTable = PrettyTable(field_names=Major.pt_hdr)
            for values in self._majors.values():
                pretty_table3.add_row(values.major_info())
            print(pretty_table3)
 
        def student_prettytable(self):
            """Sends the student data to the pretty table and prints it"""
            pretty_table1: PrettyTable = PrettyTable(field_names=Student.pt_hdr)
            for student in self._students.values():
                pretty_table1.add_row(student.student_info())
            print(pretty_table1)
 
        def instructor_prettytable(self):
            """Sends the instructors data to the pretty table and prints it"""
            pretty_table2: PrettyTable = PrettyTable(field_names=Instructor.pt_hdr)
            for instructor in self._instructors.keys():
                for c in self._instructors[instructor].instructor_info():
                    pretty_table2.add_row(c)
            print(pretty_table2)

        def student_grade_table_db(self, db_path) -> PrettyTable:
            """Student_pretty_grade_df file uses the dblink to retrive data from the database and then prints it using pretty table. """
            db: sqlite3.Connection = sqlite3.connect(db_path)
            query:str= "select students.Name as Student_Name, students.CWID, grades.Course, grades.Grade, instructors.Name as Instructor_Name \
                    from ((students inner join grades on students.CWID = grades.StudentCWID) \
                    inner join instructors on grades.InstructorCWID = instructors.CWID) order by Student_Name ASC"
            pt = PrettyTable(field_names = ["Student's Name", 'Cwid', 'Course', 'Grade', "Instructor's Name"])
            for row in db.execute(query):
                pt.add_row(row)
            print(pt)
            
def file_reader(path: str, fields: int, sep = ',', header = False) -> Iterator[Tuple[str]]:
    """ reading all the fields in a file using generator """
    try:
        fp: IO = open(path, 'r', encoding='utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"Can not open {path}")
    else:
        with fp:
            for offset, line in enumerate(fp, 1):
                current_line: list = line.rstrip('\n').split(sep)
                if len(current_line) != fields:
                    raise ValueError(f"{fp} has {len(current_line)} fields on line {offset} but expected {fields}")
                elif offset == 1 and header:
                    continue
                else:
                    yield tuple(current_line)           
        
def main():
    """ define the repositiry  """
    stevens: University = University(r'C:\Users\aryan\Documents\SSW 810\11th Assingment')

    stevens.major_prettytable()
    stevens.student_prettytable()
    stevens.instructor_prettytable()
    stevens.student_grade_table_db(r'C:\Users\aryan\Documents\SSW 810\11th Assingment\hw11')

if __name__ == "__main__":
    main()
