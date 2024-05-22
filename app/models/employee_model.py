from pydantic import BaseModel

class AcceptJoiningRequest(BaseModel):
    id: str
    emp_type: str

class RejectJoiningRequest(BaseModel):
    id: str

class RemoveEmployee(BaseModel):
    emp_id: str

class RemoveManager(BaseModel):
    manager_id: str

class UpdateSkill(BaseModel):
    emp_id: str
    skills: str

class RequestForEmployee(BaseModel):
    emp_id: str
    project_id: str

class Employee(BaseModel):
    emp_id: str
    emp_name : str
    password: str
    admin_id: str
    admin_name: str
    email: str
    mobile: str
    gender: str
    skills : str
    
class Manager(BaseModel):
    manager_id: str
    manager_name: str
    password: str
    admin_id: str
    admin_name: str
    email: str
    mobile: str
    gender: str

class Admin(BaseModel):
    admin_id : str
    admin_name: str
    password: str
    email: str
    mobile: str
    gender: str

class ManagerRequestForEmployees(BaseModel):
    emp_id:str
    manager_id: str
    project_id: str
    admin_id: str
    status: str

class EmployeeTerminationRecords(BaseModel):
    id: str
    name : str
    emp_type: str
    admin_id: str
    admin_name: str
    email: str
    mobile: str
    gender: str
    date_of_joining: str
    departure_date : str