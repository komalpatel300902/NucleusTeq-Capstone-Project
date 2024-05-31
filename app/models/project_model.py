"""
To use, simply use 'import project_model'

This module defines a various class inheriting BaseModel for holding project data. 
"""
from pydantic import BaseModel

class ProjectDetails(BaseModel): 
    project_id: str
    project_name: str 
    dead_line: str
    description: str 
    assign_to: str
    admin_id: str

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

class UnassignProjectToEmployee(BaseModel):
    emp_id: str

class UnassignProjectToManager(BaseModel):
    manager_id: str
    project_id: str

class Project_Update_Status(BaseModel):
    manager_id: str
    project_id: str
    status: str

