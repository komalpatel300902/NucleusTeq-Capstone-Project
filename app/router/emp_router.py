"""
To use, simply 'import emp_router'

This module holds all the functionalities that a employee has.
1. Employee Login Panal
2. View all employee
3. View project he/she has
4. Update the skill
5. Logout
""" 

import json
from fastapi import APIRouter, HTTPException , Request, status , Depends , Response
from fastapi .templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from models.employee_model import UpdateSkill
from models.index_model import LoginDetails
from config.db_connection import get_db
from config.password_security import check_password , hash_password
from schema.schemas import DataFormatter
import logging
from logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
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
    if employee_user.is_authenticated():
        return employee_user.employee_id
    else:
        raise HTTPException(status_code=401, detail="Unauthoroised User")

templates = Jinja2Templates(directory="templates/employee")

@emp_router.get("/employee_login")
async def employee_login(request :Request):
    """    
    Employee Login Page

    Args:
        request (Request): Holds information of incomming HTTP request.

    Returns:
        [text/html] : index.html
    """
    logger.info("Accessed Employee Login Page")
    return templates.TemplateResponse("index.html",{"request":request})


@emp_router.post(r"/employee_login", response_class = HTMLResponse)
async def employee_credential_authentication(response: Response,request : Request, login_details: LoginDetails , db = Depends(get_db)) :
    """    
    Employee Credential will be Authenticated here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        login_detail (LoginDetail): Fetch username and Password.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json :{"message":"Login Successful"}
    
    Raises:
        HTTPException [status_code = 500] : Error executing query.
        HTTPException [status_code = 401] : Username or Password is Incorrect.
    """
    logger.info(f"Attempting to authenticate Employee: {login_details.username}")
    sql, cursor = db
    sql_query_to_check_employee = f"""SELECT COUNT(emp_id) ,emp_id, password 
    FROM employees
    WHERE emp_id = '{login_details.username}';
    """
    logger.debug(f"SQL Query to Check Wheather Employee Record Exist or Not : {sql_query_to_check_employee}")

    print( "emp" , login_details.username , login_details.password )
    try:
        cursor.execute(sql_query_to_check_employee)
        data = cursor.fetchall()
        logger.info(f"Authentication query executed successfully for admin: {login_details.username}")

    except Exception as e:
        logger.error(f"Error executing authentication query: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while executing authentication query")
    
    else:
        condition = data[0][0]
        password = data[0][2]
        print(condition)
        if condition and check_password(login_details.password, password):
            logger.info(f"Employee {login_details.username} authenticated successfully.")

            employee_user.login(login_details.username)
            logger.info("Employee id is saved as SessionUser")
            logger.info(f"Redirecting to Employee home ")

            return JSONResponse(content={"message":"Login Successful"})
        else:
            logger.warning(f"Invalid login attempt for admin: {login_details.username}")
            raise HTTPException(status_code=401, detail="Invalid username or password")


@emp_router.get("/employee_home")
async def employee_home(request :Request, emp_id = Depends(get_user)):
    """    
    Employee Home Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        emp_id (String): Fetch emp_id from UserSession.
       
    Returns:
        [text/html] :home.html

    """
    logger.info(f"{emp_id} : Accessed Employee Home Page")
    return templates.TemplateResponse("home.html",{"request":request})


@emp_router.get(r"/all_colleague")
async def fetch_all_workers_for_project(request: Request,emp_id = Depends(get_user), db = Depends(get_db)) :
    """    
    View all Employee Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        emp_id (String): Fetch emp_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] :all_employee.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """
    logger.info(f"{emp_id} : Accessed View All Employee Page")
    sql, cursor = db

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
    logger.debug(f"SQL Query to fetch details of all Employee : {sql_query_to_get_all_information}")

    sql_query_to_get_manager_information = f"""SELECT m.manager_id, m.manager_name, m.gender, m.email,m.admin_id,a.admin_name , GROUP_CONCAT(mpd.project_id) , GROUP_CONCAT(p.project_name)
    FROM manager AS m
    LEFT JOIN manager_project_details AS mpd
    ON m.manager_id = mpd.manager_id
    LEFT JOIN project AS p
    ON p.project_id = mpd.project_id
    LEFT JOIN admin AS a
    ON a.admin_id = m.admin_id
    GROUP BY m.manager_id ;"""
    logger.debug(f"[Query 2] : SQL Query to Fetch all the Managers Information")

    table_column = ["emp_id", "emp_name","gender","email","admin_id","admin_name","manager_id","manager_name","project_id","project_name"]
    table_column_manager_information = ["manager_id", "manager_name","gender","email","admin_id","admin_name","project_id","project_name"]
    
    try:
        cursor.execute(sql_query_to_get_all_information)
        table_data = cursor.fetchall()
        logger.info("Data Fetched Successfully")

        cursor.execute(sql_query_to_get_manager_information)
        table_data_for_manager = cursor.fetchall()
        logger.info("Data Fetched Successfully")

        data_formatter = DataFormatter()
        managers = data_formatter.dictionary_list(table_data = table_data_for_manager, table_column=table_column_manager_information)
        data_entries = data_formatter.dictionary_list(table_data = table_data, table_column=table_column)
        logger.info("Data Formatted Successfully. Redy for sending it to WebPage")

    except Exception as e:
        logger.error(f"Error executing query or While formatting the Data: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while rendering view all employee page")
    
    else:
        return templates.TemplateResponse("all_employees.html",{"request":request, "data_entries": data_entries, "managers": managers})


@emp_router.get(r"/update_skills_as_employee")
async def update_skills_as_employee(request : Request , emp_id: str = Depends(get_user), db = Depends(get_db)) : 
    """    
    Update Skill Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        emp_id (String): Fetch emp_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] :update_skill.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """
    logger.info(f"{emp_id} : Accessed Update Skill As Employee Page")
    sql, cursor = db
    sql_query_to_fetch_employee_details = f"""SELECT emp_id , emp_name , gender , mobile , email , skills
    FROM employees WHERE emp_id = '{emp_id}' ;"""
    logger.debug(f"SQL Query to fetch Employee details : {sql_query_to_fetch_employee_details}")

    table_column = ["emp_id", "emp_name","gender","mobile","email","skills"]
    try:
        cursor.execute(sql_query_to_fetch_employee_details)
        table_data = cursor.fetchall()
        data_formatter = DataFormatter()
        employees = data_formatter.dictionary_list(table_data = table_data, table_column=table_column)
        logger.info("Data formatted successfully. Ready for sending it to Webpage")
    except Exception as e:
        logger.error(f"Error executing query or while formatting the Data: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while rendering update skill page")
    
    else:
        return templates.TemplateResponse("update_skill.html",{"request":request, "employees": employees})

@emp_router.put(r"/add_skill",response_class=JSONResponse)
async def add_skill(request : Request, employee_data: UpdateSkill, db = Depends(get_db)) :
    """    
    Add Skill Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        employee_data (UpdateSkill): Fetch new skill and employee info.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json :{"message": "Skill added Successfully"}

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """
    logger.info("Request Recieved to add new skill")
    sql, cursor = db
    sql_query_to_add_skill = f"""
    UPDATE employees
    SET skills = CONCAT(skills,' {employee_data.skills}')
    WHERE emp_id = '{employee_data.emp_id}';
    """
    logger.debug(f"SQL Query to Update add new Skill:  {sql_query_to_add_skill}")

    print(sql_query_to_add_skill)
    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_add_skill)
        sql.commit()
        logger.debug(f"Skill Added Succcessfully")
    except Exception as e:
        sql.rollback()
        logger.error(f"Error executing query or while formatting the Data: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while adding skill")
    
    else:
        
        redirect_url = request.url_for("update_skills_as_employee")
        return JSONResponse(content = {"message": "Skill added Successfully"})

@emp_router.put(r"/replace_skill",response_class=JSONResponse)
async def replace_skill(request : Request, employee_data: UpdateSkill, db = Depends(get_db)) :
    """    
    Replace Skill Request will be Addressed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        employee_data (UpdateSkill): Fetch new skill and employee info.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json :{"message": "Skill Replaces Successfully"}

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """
    logger.info("Request Recieved to Replace the existing skill")
    sql, cursor = db

    sql_query_to_replace_skill = f"""
    UPDATE employees
    SET skills =  '{employee_data.skills}'
    WHERE emp_id = '{employee_data.emp_id}';
    """
    logger.debug(f"SQL Query to replace skill : {sql_query_to_replace_skill}")

    try:
        cursor.execute("START TRANSACTION;")
        cursor.execute(sql_query_to_replace_skill)
        sql.commit()
        logger.debug(f"Skill Replaced Succcessfully")

    except Exception as e:
        sql.rollback()
        logger.error(f"Error executing query : {e}")
        raise HTTPException(status_code=500, detail="An error occurred while replacing the skill")
    
    else:
        
        redirect_url = request.url_for("update_skills_as_employee")
        return {"message":"Skill replaced Successfully"}
    
@emp_router.get(r"/employee_project_details")
async def employee_project_details(request: Request , emp_id: str = Depends(get_user), db = Depends(get_db)) :
    """    
    View Project Employee Have Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        emp_id (String): Fetch emp_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] :employee_project.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """
    logger.info(f"{emp_id} : Accessed Employee Project Detail Page")
    sql, cursor = db

    sql_query_to_fetch_project_details = f"""SELECT p.project_id, p.project_name , p.start_date, p.dead_line, m.manager_id, m.manager_name, p.description
    FROM employee_project_details AS epd
    INNER JOIN manager AS m
    ON m.manager_id = epd.manager_id
    INNER JOIN project AS p
    ON p.project_id = epd.project_id
    WHERE emp_id = '{emp_id}';"""
    logger.debug(f"SQL Query to fetch Project Details : {sql_query_to_fetch_project_details}")

    table_column = ["project_id", "project_name","start_date","dead_line","manager_id","manager_name", "description"]
    try:
        cursor.execute(sql_query_to_fetch_project_details)
        table_data = cursor.fetchall()
        data_formatter = DataFormatter()
        project_records = data_formatter.dictionary_list(table_data = table_data, table_column=table_column)
        logger.info("Data formatted successfully. Ready for sending it to Webpage")
    except Exception as e:
        logger.error(f"Error executing query or while formatting the Data: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while rendering project record page")
    
    else:
        return templates.TemplateResponse("employee_project.html",{"request":request, "project_records": project_records})

@emp_router.post("/employee_logout",response_class = HTMLResponse)
async def logout(request: Request):
    employee_user.logout()
    logger.info("Employee successfully logged out.")
    return JSONResponse(content = {"message": "User Successfully Logout"})