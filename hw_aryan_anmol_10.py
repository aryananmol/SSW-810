"""
Classes for creating a University repository which stores information for students and instructors
"""

import os
from collections import defaultdict, Counter
from typing import List, Tuple, DefaultDict, Iterator
from prettytable import PrettyTable

class Students:
    """
    Store student information:-
    CWID
    NAME
    MAJOR
    COURSES
    GPA
    """

    def __init__(self, cwid: str, name: str,  major: str, required: List, electives: List) -> None:
        """class constructor"""
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._remaining_required: List[str] = required.copy()
        self._remaining_electives: List[str] = electives.copy()
        self._courses: Dict[str, float] = dict()

    def store_course_grade(self, course: str, grade: float) -> None:
        """store information for grades scored by the student"""
        self._courses[course] = grade
        if grade > 0:
            if course in self._remaining_required:
                self._remaining_required.remove(course)
            elif course in self._remaining_electives:
                self._remaining_electives = list()
                #self._remaining_electives.append("NO course left")

    def calculate_gpa(self) -> float:
        """calculate the grade point of the students on a 4 point scale"""
        return round((sum(self._courses.values()) / len(self._courses)), 2)

    def pt_row(self) -> List:
        """return student information for pretty table"""
        return [self._cwid, self._name, self._major, list(self._courses.keys()), self._remaining_required,
                self._remaining_electives, self.calculate_gpa()]


class Instructors:
    """Store Instructor Inforamtion"""
    def __init__(self, insid:str, name:str, major:str )-> None:
        """class constructor"""
        self._insid: str = insid
        self._name: str = name
        self._majors: str = major
        self._courses: DefaultDict[str, str] = defaultdict(int) #Key Course_value:str with grade

    def store_student_course(self, course:str) -> None:
        """Store course data"""
        self._courses[course] += 1

    def pt_rows(self)-> Iterator[Tuple[str, str, str, int]]:
        """generator to add rows to pretty table"""
        for course, count in self._courses.items():
            yield self._insid, self._name, self._majors, course, count

class Major:
    """
    Store Course information:-
    Required Courses aka CORE
    Optional courses aka Electives
    """

    def __init__(self):
        """Class constructor to Store core and elective couses  """
        self._required: List = list()
        self._electives: List = list()

    def add_course(self, type_course: str, course: str) -> None:
        """ stores required and elective courses """
        if type_course == "R":
            self._required.append(course)
        else:
            self._electives.append(course)

    def get_required(self):
        """return the the core course"""
        return self._required

    def get_electives(self):
        """return the elective course"""
        return self._electives


class University:
    """University stores students and instructors at for the university and print pretty table"""
    GRADES = {"A": 4.0, "A-": 3.75, "B+": 3.25, "B": 3.0, "B-": 2.75, "C+": 2.25, "C": 2.0, "C-": 0, "D+": 0, "D": 0,
                 "D-": 0, "F": 0}

    def __init__(self, path: str) -> None:
        """store students, instructors and pretty table"""
        self._path: str = path
        self._students: Dict[str, _Student] = dict()  # _students[cwid] = Student()
        self._instructors: Dict[str, Instructor] = dict()  # _instructors[cwid] instructors()
        self._majors: Dict[str, _Major] = dict()  # _instructors[cwid] instructors()
        self._read_major(os.path.join(self._path, 'majors.txt'))
        self._read_students(os.path.join(self._path, 'students.txt'))
        self._read_instructors(os.path.join(self._path, 'instructors.txt'))
        self._read_grades(os.path.join(self._path, 'grades.txt'))

    def _read_students(self, path: str) -> None:
        """read student file"""
        try:
            for cwid, name, major in file_reader(path, 3, ';', True):
                self._students[cwid] = Students(cwid, name, major,
                                                self._majors[major].get_required(),
                                                self._majors[major].get_electives())
        except(FileNotFoundError, ValueError) as e:
            print('error no file found')

    def _read_instructors(self, path='instructors.txt')-> None:
        """read files"""
        try:
            for insid, name, major in file_reader(path, 3,'|',True):
                self._instructors[insid] = Instructors(insid, name, major)
        except(FileNotFoundError, ValueError) as e:
            print('error No file found')

    def _read_major(self, path: str) -> None:
        try:
            for major, type_course, course in file_reader(path, 3, '\t', True):
                if major not in self._majors:
                    self._majors[major] = Major()
                    self._majors[major].add_course(type_course, course)
                else:
                    self._majors[major].add_course(type_course, course)
        except(FileNotFoundError, ValueError) as e:
            print('error no file found')

    def _read_grades(self, path: str) -> None:
        """read grades file"""
        try:
            for cwid, course, grade, insid in file_reader(path, 4, '|', True):

                if cwid in self._students:
                    self._students[cwid].store_course_grade(course, self.GRADES[grade])
                else:
                    print(f"Wrong data, grade for unknown student {cwid}")

                if insid in self._instructors:
                    self._instructors[insid].store_student_course(course)
                else:
                    print(f'Wrong data, grade for unknown instructor{insid}')
        except(FileNotFoundError, ValueError) as e:
            print('error no file found')

    def major_pretty_table(self) -> None:
        major_pretty_table: PrettyTable = PrettyTable(field_names=["Major", "Required Courses", "Electives"])
        for major_id in self._majors.keys():
            major_pretty_table.add_row([major_id, self._majors[major_id].get_required(), self._majors[major_id].get_electives()])
        print(major_pretty_table)

    def student_pretty_table(self)-> None:
        """Pretty Table for students"""
        student_table: PrettyTable = PrettyTable()
        student_table.field_names = ['CWID', 'Name', 'Major', 'Completed_courses', 'Remaining_Core', 'Remaining_Electives', 'GPA']
        for cwid in self._students.keys():
            student_table.add_row(self._students[cwid].pt_row())    
        print(student_table)

    def instructor_pretty_table(self)->None:
        """Pretty Table for Instructor"""
        instructor_table: PrettyTable = PrettyTable()
        instructor_table.field_names = ['INSID', 'Name', 'Major', 'Courses_Taken', 'Students']
        for instructor in self._instructors.values():
            for row in instructor.pt_rows():
                instructor_table.add_row(row)      
        print(instructor_table)

def file_reader(path:str, fields:int,sep:str =';',header:bool = False):
    try:
        fp: IO = open(path)
    except FileNotFoundError:
        print(f"File not found{path}")
    else:
        with fp:
            if header == True:
                next(fp)
            for line in fp:
                line = line.rstrip('\n')
                line = line.split(sep)
                if len(line) != fields:
                    raise ValueError(f"the given file {path} with the line {line} having {len(line)} is less than required {fields}")
                yield (tuple(line))
def main():
    """
    define the repositiry
    """
    stevens_repository: University = University(r'C:\Users\aryan\Documents\SSW 810\10thAssingment')
    stevens_repository.student_pretty_table()
    stevens_repository.instructor_pretty_table()
    stevens_repository.major_pretty_table()


if __name__ == '__main__':
    main()