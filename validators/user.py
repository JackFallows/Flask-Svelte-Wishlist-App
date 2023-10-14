import re

from validators.validation_state import ValidationState

def validate_create(user_json) -> ValidationState:
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    
    state = (
        ValidationState()
            .add_failure_if(
                condition=user_json['password1'] != user_json['password2'],
                property="password2",
                reason="Passwords do not match"
            )
            .add_failure_if(
                condition=not re.fullmatch(email_regex, user_json['email']),
                property="email",
                reason="Email is not valid"
            )
    )

    return state
