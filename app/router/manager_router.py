"""
1: able to view all the employees, manager and projects.
2: filter employees by skill and uassigned employees.
3: request employees to admin
4: see all theproject on which manager is working
"""

from fastapi import APIRouter

manager_router = APIRouter()

@manager_router.get(r"\all")
async def get_all_employees_and_project() -> None: ...

@manager_router.get(r"\filtered_employee")
async def get_filtered_employees() -> None: ...

@manager_router.put(r"\request_employee")
async def request_employee() -> None: ...

@manager_router.get(r"\projects_I_have")
async def project_i_have() -> None: ...
