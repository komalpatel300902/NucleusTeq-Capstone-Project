"""
Facility: 
1 : View all employees(manager included)
2 : UPDATE skills
3 : View all details about its project
"""

from fastapi import APIRouter , Request
from fastapi .templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from config.db_connection import sql , cursor
from schema.schemas import DataFormatter

emp_router = APIRouter()
emp_id = "EMP001"

templates = Jinja2Templates(directory="templates/employee")

@emp_router.get("/employee_login")
async def employee_login(request :Request):
    return templates.TemplateResponse("index.html",{"request":request})

@emp_router.get("/employee_home")
async def employee_home(request :Request):
    return templates.TemplateResponse("home.html",{"request":request})


@emp_router.get(r"/employee_for_project")
async def fetch_all_workers_for_project(request: Request) -> None:
    sql_query_to_get_all_information = f"""SELECT e.emp_id, e.emp_name, e.gender, e.email,e.admin_id,e.admin_name ,m.manager_id , m.manager_name , p.project_id , p.project_name
    FROM employees AS e
    LEFT JOIN employee_project_details AS epd
    ON e.emp_id = epd.emp_id
    LEFT JOIN project AS p
    ON p.project_id = epd.project_id
    LEFT JOIN manager AS m
    ON m.manager_id = epd.manager_id;"""

    table_column = ["emp_id", "emp_name","gender","email","admin_id","admin_name","manager_id","manager_name","project_id","project_name"]
    try:
        cursor.execute(sql_query_to_get_all_information)
        table_data = cursor.fetchall()
        data_formatter = DataFormatter()
        data_entries = data_formatter.dictionary_list(table_data = table_data, table_column=table_column)
    except Exception as e:
        print(e)
    else:
        return templates.TemplateResponse("all_employees.html",{"request":request, "data_entries": data_entries})


@emp_router.get(r"/update_skills_as_employee")
async def update_skills_as_employee(request : Request) -> None: 
    sql_query_to_fetch_employee_details = f"""SELECT emp_id , emp_name , gender , mobile , email , skills
    FROM employees WHERE emp_id = '{emp_id}' ;"""

    table_column = ["emp_id", "emp_name","gender","mobile","email","skills"]
    try:
        cursor.execute(sql_query_to_fetch_employee_details)
        table_data = cursor.fetchall()
        data_formatter = DataFormatter()
        employees = data_formatter.dictionary_list(table_data = table_data, table_column=table_column)
    except Exception as e:
        print(e)
    else:
        return templates.TemplateResponse("update_skill.html",{"request":request, "employees": employees})

@emp_router.get(r"/update_skills_as_employee")
async def update_skills_as_employee(request : Request) -> None: ...

@emp_router.get(r"/employee_project_details")
async def employee_project_details(request: Request) -> None:
    sql_query_to_fetch_project_details = f"""SELECT p.project_id, p.project_name , p.start_date, p.dead_line, m.manager_id, m.manager_name
    FROM employee_project_details AS epd
    INNER JOIN manager AS m
    ON m.manager_id = epd.manager_id
    INNER JOIN project AS p
    ON p.project_id = epd.project_id
    WHERE emp_id = '{emp_id}';"""

    table_column = ["project_id", "project_name","start_date","dead_line","manager_id","manager_name"]
    try:
        cursor.execute(sql_query_to_fetch_project_details)
        table_data = cursor.fetchall()
        data_formatter = DataFormatter()
        project_records = data_formatter.dictionary_list(table_data = table_data, table_column=table_column)
    except Exception as e:
        print(e)
    else:
        return templates.TemplateResponse("employee_project.html",{"request":request, "project_records": project_records})
