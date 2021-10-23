from datetime import datetime
from re import compile, search
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


def confirm_field(value: str) -> str:
    """
    Validation to prevent empty title field.
    Called by the helperfunction below;
    """
    if not value:
        raise ValueError("Please fill in missing field.")
    return value

def check_name_length(value: str) -> str:
    """
    Check the length of the name fields
    """
    if len(value) > 100:
        raise ValueError("The provided name is too large.")
    return value

def check_special_character(value: str) -> str:
    """
    Check the presence of special characters.
    """
    special_characters = compile("[\" \"@_!#$%^&*()<>'\"?/\|}{~:]")
    if special_characters.search(value) is not None:
        raise ValueError("The provided name contains space or special character(s).")
    return value

def check_short_field_length(value: str) -> str:
    """
    Check the length of the email
    """
    if len(value) > 255:
        raise ValueError("The provided email is too large.")
    return value


def check_long_field_length(value: str) -> str:
    """
    Check the length of the message
    """
    if len(value) > 2000:
        raise ValueError("The message field is too large.")
    return value


class ContactBase(BaseModel):
    """
    Base fields for contact.
    """
    firstname: str
    lastname: str
    email: EmailStr
    subject: str
    message: str
    # Custom validation for first name field
    _check_firstname = validator("firstname", allow_reuse=True)(confirm_field)
    _check_fn_length = validator("firstname", allow_reuse=True)(check_name_length)
    _check_fn_spec_chr = validator("firstname", allow_reuse=True)(check_special_character)

    # Custom validation for last name field
    _check_lastname = validator("lastname", allow_reuse=True)(confirm_field)
    _check_ln_length = validator("lastname", allow_reuse=True)(check_name_length)
    _check_ln_spec_chr = validator("lastname", allow_reuse=True)(check_special_character)
    
    # Custom validation for email field
    _check_email = validator("email", allow_reuse=True)(confirm_field)
    _check_email_length = validator("email", allow_reuse=True)(check_short_field_length)
    
    # Custom validation for message field
    _check_message = validator("message", allow_reuse=True)(confirm_field)
    _check_message_length = validator("message", allow_reuse=True)(check_long_field_length)
    
    # Custom validation for subject field.
    _check_subject = validator("subject", allow_reuse=True)(confirm_field)
    _check_subject_length = validator("subject", allow_reuse=True)(check_short_field_length)
    

class ContactCreate(ContactBase):
    """
    Fields for creating contacts.
    """
    ...

class ContactOut(ContactBase):
    """
    For Contact response.
    """
    id: Optional[int] = None
    active: bool = True
    created: Optional[datetime] = None
    