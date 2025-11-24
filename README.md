# pylab1scms
# Python lab1 Student Course Management System (scms)

A simple, file-based Student Course Management System written in Python. This application features an interactive command-line interface (CLI) for easy management of students, instructors, and courses.

## Features

*   **Interactive Command-Line Interface**: Manage the entire system through an easy-to-use, menu-driven CLI.
*   **Entity Management**: Create and manage Students, Instructors, and Courses.
*   **Student Types**: Supports different types of students, such as `Undergraduate` and `Graduate`.
*   **Course Enrollment**: Enroll and unenroll students from courses.
*   **Grading**: Assign grades to students for specific courses and calculate the average grade for a course.
*   **Instructor Assignment**: Assign instructors to courses and validate permissions for actions like grading.
*   **Data Validation**: Ensures data integrity with validation for names, emails, age, and more.
*   **Data Persistence**: Save the entire system state (students, courses, instructors) to a JSON file and load it back.
*   **Reporting**: Generate reports for courses.
*   **Search**: Find students by their email address.

## Project Structure

```
pylab1scms/
├── registry.py         # Core Registry class to manage all data and operations.
├── student.py          # Defines Student, UndergraduateStudent, and GraduateStudent classes.
├── instructor.py       # Defines the Instructor class.
├── course.py           # Defines the Course class.
├── utils.py            # Utility functions for data validation.
├── commandline.py      # The interactive command-line interface for the user.
├── reports.py          # Generates reports for courses.
├── test.py             # Unit tests for the system.
├── requirements.txt    # Lists project dependencies (none for this project).
└── scms_data.json      # Default data file for persistence.
```

## Getting Started

### Prerequisites

*   Python 3.7+

### Installation

This project uses only standard Python libraries, so no external dependencies are required.

1.  Clone the repository or download the source code.
2.  That's it! You're ready to go.

## Usage

The primary way to use this application is through its interactive command-line interface.

### Running the Application

To start the system, run the `commandline.py` script:

```sh
python commandline.py
```

The application will load any existing data from `scms_data.json` and present you with the main menu.

### Command-Line Interface

The CLI provides separate management portals for students, instructors, and courses.

*   **Student Management Portal**:
    *   Register new students.
    *   Log in as a student to enroll in/unenroll from courses and view your schedule.

*   **Instructor Management Portal**:
    *   Register new instructors.
    *   Log in as an instructor to create courses, view your assigned courses, and generate course reports.

*   **Course Management Portal**:
    *   List all available courses in the system with their details.

*   **Save and Exit**:
    *   Your data is automatically saved to `scms_data.json` when you exit the application.

### Programmatic Usage (Advanced)

You can also interact with the system's components programmatically by importing the `Registry` class into your own scripts.

```python
# Example usage
from registry import Registry
```

## Running Tests

To ensure everything is working correctly, you can run the built-in unit tests.

```sh
python test.py
```

A successful test run will output a confirmation message.
