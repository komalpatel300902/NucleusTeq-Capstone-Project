"""[Sign up , Registration]"""

from pydantic import BaseModel, validator , field_validator
from fastapi import HTTPException
import re

class JoiningRequest(BaseModel):
    id: str
    name : str
    password: str
    emp_type: str
    admin_id: str
    email: str
    mobile: str
    gender: str
    date_of_joining: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8 and len(v) > 30:
            print("Length validated")
            raise ValueError("Password must have more than equal to 8 and Less than equal to 30 letter")
        if not re.search(r'[A-Z]', v):
            print("Upper class validated")
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            print("lower class validated")
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            print("Digit validated")
            raise ValueError('Password must contain at least one digit')
        return v
    
    @field_validator('email')
    def validate_email(cls, v):
    
        if not re.search(r'@nucleusteq.com$', v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

    @field_validator('mobile')
    def validate_mobile(cls, v):
    
        if not len(v) == 10:
            raise HTTPException(status_code=422,detail='Length of mobile number must be 10')
        if not re.search(r"[0-9]{10}",v):
            raise HTTPException(status_code=422, detail='Mobile number must be digit')
        return v
    

    


class LoginDetails(BaseModel):
    username: str
    password: str