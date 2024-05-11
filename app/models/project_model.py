from pydantic import BaseModel

class ProjectDetails(BaseModel): 
    project_id: str
    project_name: str 
    admin_id: str
    admin_name: str
    start_date: str
    dead_line: str
    status: str
    project_assigned: str
    project_completion_date: str
    description: str 

class ManagerProjectDetails(BaseModel):
    project_id: str
    manager_id: str

class EmployeeProjectDetails(BaseModel):
    emp_id: str
    project_id: str
    manager_id: str

class ManagerRequestForEmployees(BaseModel):
    emp_id:str
    manager_id: str
    project_id: str
    admin_id: str
    status: str
