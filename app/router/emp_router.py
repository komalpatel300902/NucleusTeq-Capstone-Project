"""
Facility: 
1 : View all employees(manager included)
2 : UPDATE skills
3 : View all details about its project
"""

import json
from fastapi import APIRouter, HTTPException , Request, status , Depends , Response
from fastapi .templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from models.employee_model import UpdateSkill
from models.index_model import LoginDetails
from config.db_connection import sql, cursor
from schema.schemas import DataFormatter


emp_router = APIRouter()

class EmployeeUserSession:
    def __init__(self):
        self.employee_id = None
    
    def login(self, username):
        self.employee_id = username
    
    def logout(self):
        self.employee_id = None
    
    def is_authenticated(self):
        return self.employee_id is not None
employee_user = EmployeeUserSession()
def get_user():
    return employee_user.employee_id

templates = Jinja2Templates(directory="templates/employee")

@emp_router.get("/employee_login")
async def employee_login(request :Request):
    return templates.TemplateResponse("index.html",{"request":request})


@emp_router.post(r"/employee_login_data", response_class = HTMLResponse)
async def login(response: Response,request : Request, login_details: LoginDetails ) -> None:

    sql_query_to_check_employee = f"""SELECT COUNT(emp_id) ,emp_id, password 
    FROM employees
    WHERE emp_id = '{login_details.username}' AND password = '{login_details.password}' ;
    """
    print( login_details.username , login_details.password )
    try:
        cursor.execute(sql_query_to_check_employee)
        data = cursor.fetchall()
    except Exception as e:
        print(e)
    else:
        condition = data[0][0]
        print(condition)
        if condition:
            employee_user.login(login_details.username)
            
            return JSONResponse(content={"message":"Login Successful"})
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")


@emp_router.get("/employee_home")
async def employee_home(request :Request):
    return templates.TemplateResponse("home.html",{"request":request})


@emp_router.get(r"/employee_for_project")
async def fetch_all_workers_for_project(request: Request) -> None:


    sql_query_to_get_all_information = f"""SELECT e.emp_id, e.emp_name, e.gender, e.email,e.admin_id,a.admin_name ,m.manager_id , m.manager_name , p.project_id , p.project_name
    FROM employees AS e
    LEFT JOIN employee_project_details AS epd
    ON e.emp_id = epd.emp_id
    LEFT JOIN project AS p
    ON p.project_id = epd.project_id
    LEFT JOIN manager AS m
    ON m.manager_id = epd.manager_id
    LEFT JOIN admin AS a
    ON a.admin_id = e.admin_id;"""

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
async def update_skills_as_employee(request : Request , emp_id: str = Depends(get_user)) -> None: 

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

@emp_router.put(r"/add_skill",response_class=JSONResponse)
async def add_skill(request : Request, employee_data: UpdateSkill) -> None:
    sql_query_to_add_skill = f"""
    UPDATE employees
    SET skills = CONCAT(skills,' {employee_data.skills}')
    WHERE emp_id = '{employee_data.emp_id}';
    """
    print(sql_query_to_add_skill)
    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_add_skill)
        
    except Exception as e:
        sql.rollback()
        print(e)
    else:
        sql.commit()
        redirect_url = request.url_for("update_skills_as_employee")
        return JSONResponse(content = {"message": "Skill added Successfully"})

@emp_router.put(r"/replace_skill",response_class=JSONResponse)
async def replace_skill(request : Request, employee_data: UpdateSkill) -> None:

    sql_query_to_replace_skill = f"""
    UPDATE employees
    SET skills =  '{employee_data.skills}'
    WHERE emp_id = '{employee_data.emp_id}';
    """
    try:
        cursor.execute("START TRANSACTION;")
        cursor.execute(sql_query_to_replace_skill)
        
    except Exception as e:
        sql.rollback()
        print(e)
    else:
        sql.commit()
        redirect_url = request.url_for("update_skills_as_employee")
        return {"message":"Skill replaced Successfully"}
    
@emp_router.get(r"/employee_project_details")
async def employee_project_details(request: Request , emp_id: str = Depends(get_user)) -> None:

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

@emp_router.post("/employee_logout",response_class = HTMLResponse)
async def logout(request: Request):
    employee_user.logout()
    return JSONResponse(content = {"message": "User Successfully Logout"})