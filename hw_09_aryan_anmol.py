"""University Student Repository """

import os
from typing import List, Tuple, DefaultDict, Iterator
from collections import defaultdict
from collections import Counter
from prettytable import PrettyTable

class Students:
    """Store Student Inforamtion"""
    def __init__(self, cwid:str, name:str, major:str )-> None:
        """class constructor"""
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict = dict()
    def store_course_grade(self, course: str, grade:str)-> None:
        """Adding course to grades"""
        self._courses[course] = grade

    def pt_row(self) -> Tuple[str, str, List[str]]:
        """Add rows in pretty table """
        return self._cwid, self._name, sorted(self._courses.keys())


class Instructors:
    """Store Instructor Inforamtion"""
    def __init__(self, insid:str, name:str, major:str )-> None:
        """class constructor"""
        self._insid: str = insid
        self._name: str = name
        self._major: str = major
        self._courses: DefaultDict[str, str] = defaultdict(int) #Key Course_value:str with grade

    def store_student_course(self, course:str) -> None:
        """Store course data"""
        self._courses[course] += 1

    def pt_rows(self)-> Iterator[Tuple[str, str, str, int]]:
        """generator to add rows to pretty table"""
        for course, count in self._courses.items():
            yield self._insid, self._name, self._major, course, count

class Major:
    """Store information about student majors"""
    def __init__(self):
        """Class constructor for major class to store data about student major"""
        self._core
        self._electives

class University:
    """
    Repository too store students instructors 
    for university and print pretty table
    """
    def __init__(self,path:str)-> None:
        """
        store students and  instructors
        """
        self._path: str = path #Working Directory
        self._students:Dict[str, Students] = dict() #Keys= CWID :Value = _Students()
        self._instructors:Dict[str, Instructors] = dict() #Keys= INSID :Value= _instructors()
        self._read_students()
        self._read_instructors()
        self._read_grades()

    def _read_students(self, path='students.txt')-> None:
        """read files"""
        try:
            for cwid, name, major in file_reader(os.path.join(path), fields=3,header = False, sep=';'):
                self._students[cwid] = Students(cwid, name, major)
        except(FileNotFoundError, ValueError) as e:
            print('error No file found')
        
    def _read_instructors(self, path='instructors.txt')-> None:
        """read files"""
        try:
            for insid, name, major in file_reader(os.path.join(path), fields=3,sep='|',header = False):
                self._instructors[insid] = Instructors(insid, name, major)
        except(FileNotFoundError, ValueError) as e:
            print('error No file found')

    def _read_grades(self,path='grades.txt')-> None:
        """read fles"""
        try:
            for cwid, course_name, grade, insid in file_reader(os.path.join(path), fields=4,sep='|',header = False):
                if cwid in self._students:
                    self._students[cwid].store_course_grade(course_name, grade)
                else:
                    print(f'Wrong data , grade for unknown student"{cwid}"')
                if insid in self._instructors:
                    self._instructors[insid].store_student_course(course_name)
                else:
                    print(f'Wrong data, grade for unknown instructor"{insid}"')        
        except(FileNotFoundError, ValueError) as e:
            print('error No file found')

    def student_pretty_table(self)-> None:
        """Pretty Table for students"""
        student_table: PrettyTable = PrettyTable()
        student_table.field_names = ['CWID', 'Name', 'Courses_Taken']
        for student in self._students.values():
            student_table.add_row(student.pt_row())    
        print(student_table)
    
    def instructor_pretty_table(self)->None:
        """Pretty Table for Instructor"""
        instructor_table: PrettyTable = PrettyTable()
        instructor_table.field_names = ['INSID', 'Name', 'Major', 'Courses_Taken', 'Students']
        for instructor in self._instructors.values():
            for row in instructor.pt_rows():
                instructor_table.add_row(row)      
        print(instructor_table)



def file_reader(path:str, fields:int, header:bool = False , sep:str =';'):
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

if __name__ == "__main__":
    main()