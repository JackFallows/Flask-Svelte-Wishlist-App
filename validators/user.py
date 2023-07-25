import re

def validate(user_json):
    if user_json['password1'] != user_json['password2']:
        return False, "Passwords do not match"
    
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(email_regex, user_json['email']):
        return False, "Email is not valid"
    
    return True, "Valid"
