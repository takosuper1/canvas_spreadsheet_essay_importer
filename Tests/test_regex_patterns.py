import re
import unittest


class TestRegexPatterns(unittest.TestCase):

    def setUp(self):
        """Set up the regex patterns"""
        self.essay_re = re.compile(r'^.*essay.*$', re.IGNORECASE)
        self.student_id_re = re.compile(r'^(?:student[_\s]?id|id)$', re.IGNORECASE)
        self.student_name_re = re.compile(r'^(?:student[_\s]?name|name)$', re.IGNORECASE)

    # Essay Pattern Tests
    def test_essay_lowercase(self):
        self.assertTrue(self.essay_re.match('essay'))

    def test_essay_uppercase(self):
        self.assertTrue(self.essay_re.match('ESSAY'))

    def test_essay_mixedcase(self):
        self.assertTrue(self.essay_re.match('Essay'))

    def test_essay_with_prefix(self):
        self.assertTrue(self.essay_re.match('final_essay'))

    def test_essay_with_suffix(self):
        self.assertTrue(self.essay_re.match('essay_title'))

    def test_essay_with_both(self):
        self.assertTrue(self.essay_re.match('student_essay_1'))

    def test_essay_camelcase(self):
        self.assertTrue(self.essay_re.match('MyEssay123'))

    def test_essay_no_match(self):
        self.assertFalse(self.essay_re.match('assignment'))
        self.assertFalse(self.essay_re.match('writing'))

    # Student ID Pattern Tests
    def test_student_id_underscore(self):
        self.assertTrue(self.student_id_re.match('student_id'))

    def test_student_id_camelcase(self):
        self.assertTrue(self.student_id_re.match('StudentID'))
        self.assertTrue(self.student_id_re.match('studentID'))

    def test_student_id_space(self):
        self.assertTrue(self.student_id_re.match('student id'))
        self.assertTrue(self.student_id_re.match('Student ID'))

    def test_student_id_no_separator(self):
        self.assertTrue(self.student_id_re.match('studentid'))
        self.assertTrue(self.student_id_re.match('STUDENTID'))

    def test_id_standalone(self):
        self.assertTrue(self.student_id_re.match('id'))
        self.assertTrue(self.student_id_re.match('ID'))
        self.assertTrue(self.student_id_re.match('Id'))

    def test_student_id_no_match_other_ids(self):
        self.assertFalse(self.student_id_re.match('section_id'))
        self.assertFalse(self.student_id_re.match('user_id'))
        self.assertFalse(self.student_id_re.match('course_id'))
        self.assertFalse(self.student_id_re.match('assignment_id'))

    def test_student_id_no_match_with_prefix(self):
        self.assertFalse(self.student_id_re.match('my_student_id'))

    # Student Name Pattern Tests
    def test_student_name_underscore(self):
        self.assertTrue(self.student_name_re.match('student_name'))

    def test_student_name_camelcase(self):
        self.assertTrue(self.student_name_re.match('StudentName'))
        self.assertTrue(self.student_name_re.match('studentName'))

    def test_student_name_space(self):
        self.assertTrue(self.student_name_re.match('student name'))
        self.assertTrue(self.student_name_re.match('Student Name'))

    def test_student_name_no_separator(self):
        self.assertTrue(self.student_name_re.match('studentname'))
        self.assertTrue(self.student_name_re.match('STUDENTNAME'))

    def test_name_standalone(self):
        self.assertTrue(self.student_name_re.match('name'))
        self.assertTrue(self.student_name_re.match('Name'))
        self.assertTrue(self.student_name_re.match('NAME'))

    def test_student_name_no_match_compounds(self):
        self.assertFalse(self.student_name_re.match('username'))
        self.assertFalse(self.student_name_re.match('lastname'))
        self.assertFalse(self.student_name_re.match('firstname'))
        self.assertFalse(self.student_name_re.match('filename'))
        self.assertFalse(self.student_name_re.match('first_name'))
        self.assertFalse(self.student_name_re.match('last_name'))

    def test_student_name_no_match_with_prefix(self):
        self.assertFalse(self.student_name_re.match('my_student_name'))


if __name__ == '__main__':
    # Run the tests with verbose output
    unittest.main(verbosity=2)