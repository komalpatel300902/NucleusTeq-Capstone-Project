from pydantic import BaseModel

class ProjectDetails(BaseModel): 
    project_id: str
    project_name: str 
    dead_line: str
    description: str 
    assign_to: str

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

class AssignProjectToEmployee(BaseModel):
    emp_id : str
    project_id : str

class AssignProjectToManager(BaseModel):
    manager_id : str
    project_id : str

class UnassignPtojectToEmployee(BaseModel):
    emp_id: str

class UnassignPtojectToManager(BaseModel):
    manager_id: str
    project_id: str