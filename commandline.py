from  registry import Registry
from utils import validate_email, valid_age, valid_year
from reports import CourseReport

def main():
    registry = Registry()
    registry.load_from_file()

    while True:
        print("=========Student Course Management System=========\nCommandline interface \nMenu:")
        print("1. Student Management Portal")
        print("2. Instructor Management Portal")
        print("3. Course Management Portal")
        print("4. Save and Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            student_management_portal(registry)
        elif choice == "2":
            instructor_management_portal(registry)
        elif choice == "3":
            course_management_portal(registry)
        elif choice == "4":
            registry.save_to_file()
            print("Data saved. Goodbye! and see you next time.\nexit........")
            break
        else:
            print("Invalid choice. Please try again.")
        
# Student Management Portal
def student_management_portal(registry: Registry):
    while True:
        print("---=== Student Management Portal ===---")
        print("1. Register")
        print("2. Login")
        print("3. Back to Main Menu")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            name = input("Enter student name: ").strip()
            email = input("Enter student email: ").strip()
            age = input("Enter student age: ").strip()
            year = input("Enter student year: ").strip()
            if not validate_email(email) or not valid_age(age) or not valid_year(year):
                print("Invalid input. Please try again.")
                continue
            student_id = registry.add_student(name, email, age, year)
            print(f"Student added with ID: {student_id}")
        
        elif choice == "2":
            students = registry.list_students()
            if not students:
                print("No students found.")
            else:
                for student in students.values():
                    print(f"ID: {student.id}, Name: {student.name}, Email: {student.email}, Enrolled Courses: {student.enrolled_courses}")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
            
def student_menu(registry, student):
    while True:
        print(f"---=== Student Menu for {student.name} ===---")
        print("1. Enroll in a Course")
        print("2. Unenroll from a Course")
        print("3. View Enrolled Courses")
        print("4. Back to Student Management Portal")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            course_id = input("Enter course ID to enroll: ").strip()
            try:
                registry.enroll_student_in_course(student.id, int(course_id))
                print(f"Enrolled in course {course_id} successfully.")
            except ValueError as e:
                print(e)
        
        elif choice == "2":
            course_id = input("Enter course ID to unenroll: ").strip()
            try:
                registry.unenroll_student_from_course(student.id, int(course_id))
                print(f"Unenrolled from course {course_id} successfully.")
            except ValueError as e:
                print(e)
        
        elif choice == "3":
            enrolled_courses = student.enrollments
            if not enrolled_courses:
                print("No enrolled courses.")
            else:
                for enrollment in enrolled_courses:
                    print(f"Course ID: {enrollment['course_id']}")
        
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
            
            
def instructor_management_portal(registry: Registry):
    while True:
        print("---=== Instructor Management Portal ===---")
        print("1. Register")
        print("2. Login")
        print("3. Back to Main Menu")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            name = input("Enter instructor name: ").strip()
            email = input("Enter instructor email: ").strip()
            instructor_id = registry.add_instructor(name, email)
            print(f"Instructor added with ID: {instructor_id}")
        
        elif choice == "2":
            instructors = registry.list_instructors()
            if not instructors:
                print("No instructors found.")
            else:
                for instructor in instructors.values():
                    print(f"ID: {instructor.id}, Name: {instructor.name}, Email: {instructor.email}, Assigned Courses: {instructor.assigned_courses}")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
            
            
def instructor_menu(registry, instructor):
    while True:
        print(f"---=== Instructor Menu for {instructor.name} ===---")
        print("1. create Course")
        print("2. View my Courses")
        print("3. generate Course Report")
        print("4. Back to Instructor Management Portal")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            title = input("Enter course title: ").strip()
            desc = input("Enter course description: ").strip()
            year = input("Enter course year: ").strip()
            if not valid_year(year):
                print("Invalid year. Please try again.")
                continue
            course = registry.create_course(title, desc, int(year), instructor.id)
            print(f"Course created {course.title} with ID: {course.id}")
        
        elif choice == "2":
            assigned_courses = instructor.courses
            if not assigned_courses:
                print("No assigned courses.")
            else:
                for course_id in assigned_courses:
                    course = registry.get_course(course_id)
                    print(f"Course ID: {course.id}, Title: {course.title}, Description: {course.description}, Year: {course.year}")
                    
        
        elif choice == "3":
            cid = input("Enter course ID to generate report: ").strip()
            if cid.isdigit() and int(cid) in instructor.courses:
                course = registry.get_course(int(cid))
                report = CourseReport(registry, int(cid))
                report.generate()
            else:
                print("Invalid course ID or you are not assigned to this course.")
                
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
            
            
def course_management_portal(registry: Registry):
    while True:
        print("---=== Course Management Portal ===---")
        print("1. List all Courses")
        print("2. Back to Main Menu")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            courses = registry.list_courses()
            if not courses:
                print("No courses found.")
            else:
                for course in courses.values():
                    instructor = registry.get_instructor(course.instructor_id) if course.instructor_id else None
                    instructor_name = instructor.name if instructor else "No Instructor Assigned"
                    print(f"ID: {course.id}, Title: {course.title}, Description: {course.description}, Year: {course.year}, Instructor: {instructor_name}")
        
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")
            
            
if __name__ == "__main__":
    main()
