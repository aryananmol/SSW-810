import unittest

from hw_aryan_anmol_10 import University


class MyTestCase(unittest.TestCase):
    def test_University(self):
        stevens: University = University(r'C:\Users\aryan\Documents\SSW 810\10thAssingment')
        self.assertEqual(stevens._students["10115"].pt_row(), ['10115', 'Wyatt, X', 'SFEN',
                                                             ['SSW 567', 'SSW 564', 'SSW 687', 'CS 545'],
                                                             ['SSW 540', 'SSW 555'], [], 3.81])
        self.assertEqual(stevens._students["11399"].pt_row(),
                         ["11399", "Cordova, I", "SYEN", ['SSW 540'], ['SYS 671', 'SYS 612', 'SYS 800'], [], 3.0])
        self.assertNotEqual(stevens._students["10115"].pt_row(), ('10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567']))
        self.assertNotEqual(stevens._students["11399"].pt_row(), ('11399', 'Cordova, I', ['CS 540']))
        self.assertEqual(stevens._majors["SFEN"]._required, ['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567'])
        self.assertNotEqual(stevens._majors["SFEN"]._required, ['SSW 564', 'SSW 555', 'SSW 567'])
        self.assertEqual(stevens._majors["SFEN"]._electives, ['CS 501', 'CS 513', 'CS 545'])
        self.assertNotEqual(stevens._majors["SFEN"]._electives, ['CS 501', 'CS 545'])
        self.assertEqual(stevens._majors["SYEN"]._required, ['SYS 671', 'SYS 612', 'SYS 800'])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)