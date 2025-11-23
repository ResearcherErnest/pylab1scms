from abc import ABC, abstractmethod
from typing import List

class ReportBase(ABC):
    @abstractmethod
    def generate(self) -> List[str]:
        pass
    
class CourseReport(ReportBase):
    def __init__(self, course, students_lookup):
        self.course = course
        self.students_lookup = students_lookup
        
    def generate(self):
        print(f"Report for course name: {self.course.title} with id {self.course.id}")
        
        if not self.course.roster:
            print(f"No students enrolled in {self.course.title}")
            return
        
        for sid in self.course.roster:
            student = self.students_lookup(sid)
            grade  = self.course.grades.get(sid)
            grade_str = f"{grade:.1f}" if grade is not None else "Marks not available at moment"
            print(f"{student.id}:{student.name}:{grade_str}")
            
        avg = self.course.get_average_grade()
        if avg is not None:
            print(f"class average: {avg:.2f}")
            
        
        