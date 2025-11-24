from dataclasses import dataclass, asdict, field
from typing import List, Dict
from utils import validate_name, validate_email, valid_age, valid_year


@dataclass
class person:
    id: int
    name: str
    email: str
    age: int
    year: int
    
    def __post_init__(self):
        if not validate_name(self.name):
            raise ValueError("Invalid name: name  must contain letters spaces and apostrophes only")
        
        if not validate_email(self.email):
            raise ValueError("Invalid email address")
        
        if not valid_age(self.age):
            raise ValueError("Invalid age: age must be between 10 and 30")
                
    def to_dict(self) -> Dict:
        return asdict(self)
    
@dataclass
class Student(person):
    enrollments: List[Dict] = field(default_factory=list)
    student_type: str = "student"
    
    def enroll(self, course_id: int) -> None:
        if course_id in self.enrollments:
            raise ValueError(f"Student is already enrolled in course {course_id}")
        self.enrollments.append({"course_id": course_id})
    
    def unenroll(self, course_id: int) -> None:
        enrollment_to_remove = None
        for enrollment in self.enrollments:
            if enrollment.get("course_id") == course_id:
                enrollment_to_remove = enrollment
                break
        if enrollment_to_remove is None:
            raise ValueError(f"Student is not enrolled in course {course_id}")
        self.enrollments.remove(enrollment_to_remove)
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} student id={self.id} name={self.name} email={self.email} age={self.age} year={self.year} enrollments={self.enrollments}>"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Student) and self.id == other.id and self.email == other.email and self.name == other.name
    
@dataclass
class UndergraduateStudent(Student):
    student_type: str = "undergraduate"
    
@dataclass
class GraduateStudent(Student):
    student_type: str = "graduate"    
