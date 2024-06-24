"""
To use, simply use 'import index_model'

This module defines a various class inheriting BaseModel for holding employee data. 
"""
from pydantic import BaseModel, validator , field_validator
from fastapi import HTTPException
import re
import datetime

class JoiningRequest(BaseModel):
    """
    When employee makes a Joining Request the data is stored in this class.
    """
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
        if len(v) < 8 :
            print("Length validated")
            raise HTTPException(status_code=422,detail='Length of password must be > 8 and  < 30')
        if len(v) > 30 :
            print("Length validated")
            raise HTTPException(status_code=422,detail='Length of password must be > 8 and  < 30')
        if not re.search(r'[A-Z]', v):
            print("Upper class validated")
            raise HTTPException(status_code=422,detail='Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            print("lower class validated")
            raise HTTPException(status_code=422,detail='Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            print("Digit validated")
            raise HTTPException(status_code=422,detail='Password must contain at least one digit')
        return v
    
    @field_validator('email')
    def validate_email(cls, v):
    
        if not re.search(r'@nucleusteq.com$', v):
            raise HTTPException(status_code=422,detail='email domain must belong to Organization')
        return v

    @field_validator('mobile')
    def validate_mobile(cls, v):
    
        if not len(v) == 10:
            raise HTTPException(status_code=422,detail='Length of mobile number must be 10')
        if not re.search(r"[0-9]{10}",v):
            raise HTTPException(status_code=422, detail='Mobile number must be digit')
        return v
 
    @field_validator('date_of_joining')
    def validate_date(cls, v):
        date = datetime.date.today().strftime("%Y-%m-%d")
        if v < date:
            raise HTTPException(status_code=422, detail="Date must be greater than yesterday's date.")

        return v
    

    


class LoginDetails(BaseModel):
    """
    When admin, manager, employee tries to log the form data is handled by this class.
    """
    username: str
    password: str