from dataclasses import dataclass, field
from typing import List, Dict, Optional
from utils import nonempty

@dataclass
class Course:
    id: int
    title: str
    description: str
    year : int
    instructor_id: Optional[int] = None
    roster: List[int] = field(default_factory=list)
    grades: Dict[int, float] = field(default_factory=dict)

    def __post_init__(self):
        if not nonempty(self.title):
            raise ValueError("Course title cannot be empty")
        if not nonempty(self.description):
            raise ValueError("Course description cannot be empty")

    def enroll_student(self, student_id: int) -> None:
        if student_id in self.roster:
            raise ValueError(f"Student {student_id} is already enrolled in course {self.id}")
        self.roster.append(student_id)

    def unenroll_student(self, student_id: int) -> None:
        if student_id not in self.roster:
            raise ValueError(f"Student {student_id} is not enrolled in course {self.id}")
        self.roster.remove(student_id)
        self.grades.pop(student_id, None)
        
    def set_grade(self, student_id: int, grade: float) -> None:
        if student_id not in self.roster:
            raise ValueError(f"Student {student_id} is not enrolled in course {self.id}")
        if grade < 0.0 or grade > 100.0:
            raise ValueError("Grade must be between 0 and 100")
        self.grades[student_id] = grade
        
    def get_average_grade(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "year": self.year,
            "instructor_id": self.instructor_id,
            "roster": self.roster,
            "grades": self.grades
        }
        
    def __repr__(self) -> str:
        return f"<Course id={self.id} title={self.title} instructor_id={self.instructor_id} roster_size={len(self.roster)}>"