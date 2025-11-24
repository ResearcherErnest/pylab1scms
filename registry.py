import json
import os
from typing import Dict, Optional
from student import Student, UndergraduateStudent, GraduateStudent
from instructor import Instructor
from course import Course

data_file = "scms_data.json"

class Registry:
    def __init__(self):
        self._students: Dict[int, Student] ={}
        self._intructors: Dict[int, Instructor] = {}
        self._courses: Dict[int, Course] = {}
        self._next_person_id: int = 1
        self._next_course_id: int = 1
        
    def create_student(self, name: str, email: str, age:int, year:int, student_type = "Student",  **kwargs) -> Student:
        if student_type.lower() == "undergraduate":
            student = UndergraduateStudent(id=self._next_person_id, name=name, email=email, age=age, year=year, **kwargs)
        elif student_type.lower() == "graduate":
            student = GraduateStudent(id=self._next_person_id, name=name, email=email, age=age, year=year, **kwargs)
        else:
            student = Student(id=self._next_person_id, name=name, email=email, age=age, year=year, **kwargs)
        self._students[self._next_person_id] = student
        self._next_person_id += 1
        return student
    
    def create_instructor(self, name: str, email: str, **kwargs) -> Instructor:
        instructor = Instructor(id=self._next_person_id, name=name, email=email, **kwargs)
        self._intructors[self._next_person_id] = instructor
        self._next_person_id += 1
        return instructor
    
    def create_course(self, title: str, description: str, instructor_id: int, year: Optional[int] = None, **kwargs) -> Course:
        if instructor_id is not None and instructor_id not in self._intructors:
            raise ValueError(f"Instructor with id {instructor_id} does not exist")
        course = Course(id=self._next_course_id, title=title, description=description, instructor_id=instructor_id, year=year, **kwargs)
        self._courses[self._next_course_id] = course
        
        if instructor_id is not None:
            self._intructors[instructor_id].assign_course(self._next_course_id)
        self._next_course_id += 1
        return course
    
    def get_student(self, student_id: int) -> Optional[Student]:
        return self._students.get(student_id)
    
    def get_instructor(self, instructor_id: int) -> Optional[Instructor]:
        return self._intructors.get(instructor_id)
    
    def get_course(self, course_id: int) -> Optional[Course]:
        return self._courses.get(course_id)
    
    def find_students_by_email(self, email: str) -> Optional[Student]:
        for student in self._students.values():
            if student.email.lower() == email.lower():
                return student
        return None
    
    def list_instructors(self) -> Dict[int, Instructor]:
        return self._intructors
    
    def list_students(self) -> Dict[int, Student]:
        return self._students
    
    def list_courses(self) -> Dict[int, Course]:
        return self._courses
    
    def enroll_student_in_course(self, student_id: int, course_id: int) -> None:
        student = self.get_student(student_id)
        course = self.get_course(course_id)
        if student is None:
            raise ValueError(f"Student with id {student_id} does not exist")
        if course is None:
            raise ValueError(f"Course with id {course_id} does not exist")
        course.enroll_student(student_id)
        student.enroll(course_id)
        
    def unenroll_student_from_course(self, student_id: int, course_id: int) -> None:
        student = self.get_student(student_id)
        course = self.get_course(course_id)
        if student is None:
            raise ValueError(f"Student with id {student_id} does not exist")
        if course is None:
            raise ValueError(f"Course with id {course_id} does not exist")
        course.unenroll_student(student_id)
        student.unenroll(course_id)
        
    def set_grade(self, instructor_id: int, course_id: int, student_id: int, grade: float) -> None:
        course = self.get_course(course_id)
        if course is None:
            raise ValueError(f"Course with id {course_id} does not exist")
        course = self._courses[course_id]
        if course.instructor_id != instructor_id:
            raise ValueError(f"Instructor with id {instructor_id} is not assigned to course {course_id}")
        course.set_grade(student_id, grade)
        
    def save_to_file(self, file_path: str = data_file) -> None:
        data = {
            "students": [student.to_dict() for student in self._students.values()],
            "instructors": [instructor.to_dict() for instructor in self._intructors.values()],
            "courses": [course.to_dict() for course in self._courses.values()],
            "next_person_id": self._next_person_id,
            "next_course_id": self._next_course_id
        }
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
            
    def load_from_file(self, file_path: str = data_file) -> None:
        if not os.path.exists(file_path):
            print(f"No data file found at {file_path}, starting with empty registry.")
            return
        
        with open(file_path, "r") as f:
            data = json.load(f)
        self._students = {student_data["id"]: Student(**student_data) for student_data in data.get("students", [])}
        self._intructors = {instructor_data["id"]: Instructor(**instructor_data) for instructor_data in data.get("instructors", [])}
        self._courses = {course_data["id"]: Course(**course_data) for course_data in data.get("courses", [])}
        self._next_person_id = data.get("next_person_id", 1)
        self._next_course_id = data.get("next_course_id", 1)
        print(f"Data loaded from {file_path}.")
        