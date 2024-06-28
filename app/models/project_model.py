"""
To use, simply use 'import project_model'

This module defines a various class inheriting BaseModel for holding project data. 
"""
from pydantic import BaseModel , field_validator
from fastapi import HTTPException
import datetime
today = datetime.date.today().strftime("%Y-%m-%d")
class ProjectDetails(BaseModel): 
    project_id: str
    project_name: str 
    dead_line: str
    tech_used: str
    description: str 
    assign_to: str
    admin_id: str

    @field_validator('dead_line')
    def check_dead_line(cls,v):
        if v <= today:
            raise HTTPException(status_code = 422, detail = "deadline must be greater than todays date")
        return v

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

