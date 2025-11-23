from dataclasses import dataclass, field
from typing import List, Dict
from utils import validate_email, validate_name

@dataclass
class Instructor:
    id: int
    name: str
    email: str
    courses: List[int] = field(default_factory=list)

    def __post_init__(self):
        if not validate_name(self.name):
            raise ValueError(f"Invalid name: {self.name}, must contain letters and may contain spaces, and apostrophes only ")
        if not validate_email(self.email):
            raise ValueError(f"Invalid email: {self.email}, must be a valid email address")

    def assign_course(self, course_id: int) -> None:
        if course_id in self.courses:
            raise ValueError(f"Instructor is already assigned to course {course_id}")
        self.courses.append(course_id)

    def unassign_course(self, course_id: int) -> None:
        if course_id not in self.courses:
            raise ValueError(f"Instructor is not assigned to course {course_id}")
        self.courses.remove(course_id)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "courses": self.courses
        }
    
    def __repr__(self) -> str:
        return f"<Instructor id={self.id} name={self.name} email={self.email} courses={self.courses}>"