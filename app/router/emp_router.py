"""
Facility: 
1 : View all employees(manager included)
2 : UPDATE skills
3 : View all details about its project
"""

from fastapi import APIRouter

emp_router = APIRouter()

@emp_router.get(r"\all")
async def fetch_all_workers() -> None: ...

@emp_router.put(r"\update_skills")
async def update_skills() -> None: ...

@emp_router.get(r"\my_project")
async def fetch_my_project_details() -> None: ...