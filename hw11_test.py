import unittest
from hw_11 import Student, Instructor, University
from typing import List
import sqlite3
""" testing different files """

class StudentTest(unittest.TestCase):
    """ Class to check class Student """
    def test_student(self) -> None:
        """ Function that tests class Student """
        actual: list = list()
        for student in University(r'C:\Users\aryan\Documents\SSW 810\11th Assingment')._students.values():            
            actual.append(student.student_info())
        expected: List[List[str, str, List[str], List[str], List[str], float]] =  \
            [('10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], ['SSW 540', 'SSW 555'], [], 3.38), 
            ('10115', 'Bezos, J', 'SFEN', ['SSW 810'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 546'], 4.00), 
            ('10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'], ['SSW 540'], ['CS 501', 'CS 546'], 4.00), 
            ('11714', 'Gates, B', 'CS', ['CS 546', 'CS 570', 'SSW 810'], [], [], 3.50)]
        
        self.assertEqual(actual, expected)


class InstructorTest(unittest.TestCase):
    """ Class to check class Instructor """
    def test_instructor(self) -> None:
        """ Function that tests class Instructor """
        actual: list = list()
        for instructor in University(r'C:\Users\aryan\Documents\SSW 810\11th Assingment')._instructors.values():
            for c in instructor._courses:
                actual.append([instructor._cwid, instructor._name, instructor._major, c, instructor._courses[c]])
        expected: List[List[str, str, str, str, int]] = \
            [['98764', 'Cohen, R', 'SFEN', 'CS 546', 1], 
            ['98763', 'Rowland, J', 'SFEN', 'SSW 810', 4], 
            ['98763', 'Rowland, J', 'SFEN', 'SSW 555', 1], 
            ['98762', 'Hawking, S', 'CS', 'CS 501', 1], 
            ['98762', 'Hawking, S', 'CS', 'CS 546', 1], 
            ['98762', 'Hawking, S', 'CS', 'CS 570', 1]]
        self.assertEqual(actual, expected)

class MajorTest(unittest.TestCase):
    """ Class to check class Major """
    def test_major(self) -> None:
        """ Function that tests class Major """
        actual: list = list()
        for major in University(r'C:\Users\aryan\Documents\SSW 810\11th Assingment')._majors.values():
            actual.append([major._major, major._required, major._electives])
        expected: List[List[str, List[str], List[str]]] = \
            [['SFEN', {'SSW 540', 'SSW 555', 'SSW 810'}, {'CS 501', 'CS 546'}], 
            ['CS', {'CS 546', 'CS 570'}, {'SSW 565', 'SSW 810'}]]
        self.assertEqual(actual, expected)

class DataBaseTest(unittest.TestCase):
    def test_student_grade_table_db(self):
            """ Function that tests class student grade database """
            dblink = r'C:\Users\aryan\Documents\SSW 810\11th Assingment\hw11'
            db: sqlite3.Connection = sqlite3.connect(dblink)
            query:str= "select students.Name as Student_Name, students.CWID, grades.Course, grades.Grade, \
                instructors.Name as Instructor_Name from ((students inner join grades on students.CWID = grades.StudentCWID) \
                    inner join instructors on grades.InstructorCWID = instructors.CWID) order by Student_Name ASC;"        
            actual = list()
            for row in db.execute(query):
                actual.append(row)
            expected = [('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'), 
            ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'), 
            ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'), 
            ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'), 
            ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'), 
            ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'), 
            ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'), 
            ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'), 
            ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J')]

            self.assertEqual(actual, expected)

class ErrorTest(unittest.TestCase):
    """ testing all the errors """
    def test_error_student(self) -> None:
        """ Function that tests Student file not found error """
        with self.assertRaises(FileNotFoundError): # raises exception error
            University("nothing to check")._read_students()
    
    def test_error_instructor(self) -> None:
        """ Function that tests Instructor file not found error """
        with self.assertRaises(FileNotFoundError): # raises exception error
            University("nothing to check")._read_instructors()
    

if __name__ == "__main__":
    unittest.main(exit = False, verbosity = 2)