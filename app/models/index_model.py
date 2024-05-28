"""[Sign up , Registration]"""

from pydantic import BaseModel, validator
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

  
    @validator('password')
    def validate_password(cls, v):
       
        if not re.search(r'[A-Z]', v):
            raise HTTPException(status_code=422, detail='Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise HTTPException(status_code=422, detail='Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise HTTPException(status_code=422, detail='Password must contain at least one digit')
        return v
    
    @validator('email')
    def validate_password(cls, v):
    
        if not re.search(r'@nucleusteq.com', v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

    @validator('mobile')
    def validate_password(cls, v):
    
        if not len(v) == 10:
            raise ValueError('Length of mobole number must be 10')
        if not re.search(r"[0-9]{10}",v):
            raise ValueError('Mobile number must be digit')
        return v
    

    


class LoginDetails(BaseModel):
    username: str
    password: str