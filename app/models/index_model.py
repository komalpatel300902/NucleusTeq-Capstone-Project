"""[Sign up , Registration]"""

from pydantic import BaseModel

class JoiningRequest(BaseModel):
    id: str
    name : str
    password: str
    emp_type: str
    admin_id: str
    admin_name: str
    email: str
    mobile: str
    gender: str
    date_of_joining: str
    status : str
    
