import unittest
import os
from registry import Registry
from student import UndergraduateStudent, GraduateStudent
from instructor import Instructor
from course import Course

class TestRegistry(unittest.TestCase):

    def setUp(self):
        """Set up a new registry for each test."""
        self.reg = Registry()
        # Create some initial data
        self.inst1 = self.reg.create_instructor("Dr Test", "dr.test@example.com")
        self.student1 = self.reg.create_student(name="john", email="john@example.com", age=15, year=3, student_type="undergraduate") # id will be 2
        self.course1 = self.reg.create_course("Python 101", "Intro to Python", self.inst1.id, year=1) # id will be 1

    def test_student_creation(self):
        """Test creation of different types of students."""
        undergrad = self.reg.create_student(name="Bob", 
                                            email="bob@example.com", 
                                            age=20,
                                            year=2, 
                                            student_type="undergraduate")
        self.assertIsInstance(undergrad, UndergraduateStudent)
        self.assertEqual(undergrad.name, "Bob")
        self.assertEqual(undergrad.student_type, "undergraduate")

        grad = self.reg.create_student(name="Charlie", email="charlie@example.com", age=22, year=1, student_type="graduate")
        self.assertIsInstance(grad, GraduateStudent)
        self.assertEqual(grad.name, "Charlie")
        self.assertEqual(grad.student_type, "graduate")

    def test_invalid_student_creation(self):
        """Test that creating a student with invalid data raises errors."""
        with self.assertRaises(ValueError, msg="Should fail with invalid name"):
            self.reg.create_student("123gad", "good@email.com", age=21, year=1, student_type="undergraduate")
        with self.assertRaises(ValueError, msg="Should fail with invalid email"):
            self.reg.create_student("Good Name", "bademail.com", age=21, year=1, student_type="undergraduate")

    def test_instructor_course_creation(self):
        """Test creating an instructor and a course."""
        self.assertIsInstance(self.inst1, Instructor)
        self.assertIsInstance(self.course1, Course)
        self.assertEqual(self.course1.instructor_id, self.inst1.id)
        self.assertIn(self.course1.id, self.inst1.courses)

    def test_enrollment(self):
        """Test enrolling a student in a course."""
        self.reg.enroll_student_in_course(self.student1.id, self.course1.id)
    
        student = self.reg.get_student(self.student1.id)
        course = self.reg.get_course(self.course1.id)

        self.assertIn(self.student1.id, course.roster)
        self.assertIn(self.course1.id, [e['course_id'] for e in student.enrollments])

        # Test enrolling in the same course again
        with self.assertRaises(ValueError):
            self.reg.enroll_student_in_course(self.student1.id, self.course1.id)

    def test_unenrollment(self):
        """Test unenrolling a student from a course."""
        self.reg.enroll_student_in_course(self.student1.id, self.course1.id)
        self.reg.unenroll_student_from_course(self.student1.id, self.course1.id)

        student = self.reg.get_student(self.student1.id)
        course = self.reg.get_course(self.course1.id)

        self.assertNotIn(self.student1.id, course.roster)
        self.assertNotIn(self.course1.id, student.enrollments)

        # Test unenrolling when not enrolled
        with self.assertRaises(ValueError):
            self.reg.unenroll_student_from_course(self.student1.id, self.course1.id)

    def test_grades(self):
        """Test setting and getting grades."""
        self.reg.enroll_student_in_course(self.student1.id, self.course1.id)
        self.reg.set_grade(self.inst1.id, self.course1.id, self.student1.id, 95.5)

        course = self.reg.get_course(self.course1.id)
        self.assertEqual(course.grades[self.student1.id], 95.5)
        self.assertAlmostEqual(course.get_average_grade(), 95.5)

    def test_grade_permissions(self):
        """Test that only the assigned instructor can set a grade."""
        other_inst = self.reg.create_instructor("Dr Impostor", "impostor@example.com")
        self.reg.enroll_student_in_course(self.student1.id, self.course1.id)

        with self.assertRaises(ValueError):
            self.reg.set_grade(other_inst.id, self.course1.id, self.student1.id, 50)

    def test_find_student_by_email(self):
        """Test finding a student by their email address."""
        found_student = self.reg.find_students_by_email("john@example.com")
        self.assertIsNotNone(found_student)
        self.assertEqual(found_student.id, self.student1.id)

        # Test case-insensitivity
        found_student_upper = self.reg.find_students_by_email("JOHN@EXAMPLE.COM")
        self.assertIsNotNone(found_student_upper)
        self.assertEqual(found_student_upper.id, self.student1.id)

        # Test not found
        not_found_student = self.reg.find_students_by_email("noone@example.com")
        self.assertIsNone(not_found_student)

    def test_persistence(self):
        """Test saving to and loading from a file."""
        test_file = "test_data.json"
        self.reg.save_to_file(test_file)
        
        new_reg = Registry()
        new_reg.load_from_file(test_file)
        
        self.assertEqual(len(self.reg.list_students()), len(new_reg.list_students()))
        self.assertEqual(len(self.reg.list_courses()), len(new_reg.list_courses()))
        self.assertEqual(self.reg._next_person_id, new_reg._next_person_id)

        # os.remove(test_file) # Clean up test file if does not cause issues by uncommenting this line

if __name__ == "__main__":
    test_result = unittest.main(exit=False)
    if test_result.result.wasSuccessful():
        print("Deal done 👏👏💪\ntest done successful and there is no error")