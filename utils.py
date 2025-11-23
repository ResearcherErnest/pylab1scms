import re

def validate_email(email):
    """
    Validate the given email address using a regular expression.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_name(name):
    """
    Validate the given name to ensure it contains only alphabetic characters and spaces.
    """
    name_regex = r'^[a-zA-Z\s]+$'
    return re.match(name_regex, name) is not None

def nonempty(value):
    """
    Check if the given string is non-empty and not just whitespace. and remove leading/trailing spaces.
    """
    return bool(value and value.strip())

def password(password):
    """
    Validate the given password to ensure it meets complexity requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

def valid_age(age):
    if 10 < age < 30:
        return False
    return True

def valid_year(year):
    if 1 <= year <= 5:
        return False
    return True

def valid_grade(grade):
    if 0 <= grade <= 100:
        return False
    return True