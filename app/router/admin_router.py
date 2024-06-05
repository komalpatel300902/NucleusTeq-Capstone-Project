"""
To use, simply 'import admin_router'

This module holds all the functionalities that a admin has.
1. Admin Login Panal
2. View all employee and project
3. Add new employee (Manager/employee)
4. Address manager request for employees
5. Assign project (manager/employee)
6. Unassign project (manager/employee)
7. Remove employee (manager/employee)
8. Update employee skill
9. create Project
10. Manager Request  for completion of project 
11. View all project
12. Logout 
""" 
from fastapi import APIRouter, HTTPException, Request , Form , status, Response , Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse , JSONResponse, RedirectResponse
from config.db_connection import get_db
from schema.schemas import DataFormatter
from models.index_model import JoiningRequest , LoginDetails
from models.employee_model import AcceptJoiningRequest , RejectJoiningRequest, RemoveEmployee,RemoveManager, UpdateSkill
from models.project_model import (ProjectDetails, 
                                  ManagerRequestForEmployees, 
                                  AssignProjectToEmployee,
                                  AssignProjectToManager, 
                                  UnassignProjectToEmployee,
                                  UnassignProjectToManager)
import json
from datetime import datetime
from logging_config import setup_logging
import logging

class UserSession:

    """
    A UserSession holds the admin_id once admin is authenticated
    """
    def __init__(self):
        self.admin_id = None
    
    def login(self, username):
        self.admin_id = username
    
    def logout(self):
        self.admin_id = None
    
    def is_authenticated(self):
        return self.admin_id is not None

setup_logging()
logger = logging.getLogger(__name__)
admin_user = UserSession()
def get_user():
    if admin_user.is_authenticated(): 
        return admin_user.admin_id
    else:
        raise HTTPException(status_code=401, detail="Unauthoroised User")

admin_router = APIRouter()


templates = Jinja2Templates(directory="templates/admin")

@admin_router.get(r"/admin_login", response_class = HTMLResponse)
async def admin_login(request : Request):
    
    """
    Starting point of the Apllication.

    Args:
        request (Request): Holds information of incomming HTTP request.

    Returns:
        [text/html]: index page
    """

    logger.info("Accessed Admin Login Page.")
    return templates.TemplateResponse("index.html",{"request":request})

@admin_router.post(r"/admin_login_data", response_class = HTMLResponse)
async def admin_credential_authentication(response: Response ,request : Request,  login_details: LoginDetails, db = Depends(get_db)) :
    
    """    
    Login Credential of admin is authenticated here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        login_details (LoginDetails): Holds the username and password of admin.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"Login Successful"}

    Raises:
        HTTPException [status_code = 500] : Error executing query.
        HTTPException [status_code = 401] : Username or Password is Incorrect.
    """
     
    logger.info(f"Attempting to authenticate admin: {login_details.username}")
    sql, cursor = db
    sql_query_to_check_admin = f"""SELECT COUNT(admin_id) ,admin_id, password 
    FROM admin
    WHERE admin_id = '{login_details.username}' AND password = '{login_details.password}' ;
    """
    logger.debug(f"SQL Query to Check Wheather Admin Record Exist or Not : {sql_query_to_check_admin}")

    print( "Admin",login_details.username , login_details.password )
    try:
        cursor.execute(sql_query_to_check_admin)
        data = cursor.fetchall()
        logger.info(f"Authentication query executed successfully for admin: {login_details.username}")

    except Exception as e:
        logger.error(f"Error executing authentication query: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while removing employee")
    
    else:
        condition = data[0][0]
        print(type(condition))
        if condition:
            logger.info(f"Admin {login_details.username} authenticated successfully.")

            admin_user.login(login_details.username)
            logger.info("Admin id is saved as SessionUser")

            redirect_url = request.url_for('admin_home')
            print(redirect_url)
            logger.info(f"Redirecting to admin home")

            return JSONResponse(content={"message":"Login Successful"})
        else:
            logger.warning(f"Invalid login attempt for admin: {login_details.username}")
            raise HTTPException(status_code=401, detail="Invalid username or password")

        
@admin_router.get("/admin_home", response_class = HTMLResponse)
async def admin_home(request: Request, admin_id = Depends(get_user)):  
    
    """
    Admin Home Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        admin_id (str): Fetch the admin id from UserSession.

    Returns:
        [text/html]: Home page of admin.
    """ 

    logger.info(f"{admin_id} : Accessed Admin Home Page.")
    return templates.TemplateResponse("home.html",{"request":request})

@admin_router.get(r"/joining_request", response_class = JSONResponse)
async def get_joining_request(request : Request, admin_id: str = Depends(get_user), db = Depends(get_db)) :
    
    """    
    Joining Request of Employee Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        admin_id (String): Fetch admin_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] : Joining request of employee page.

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"{admin_id} : Accessed Joining Request of Employee Page")
    logger.info(f"Fetching joining requests for admin: {admin_id}")
    sql,cursor = db
    try:
        
        sql_query_for_data = f"""SELECT jr.id , jr.name, jr.emp_type, jr.admin_id, jr.email, jr.mobile, jr.gender, jr.date_of_joining, a.admin_name
        FROM joining_request AS jr , admin AS a
        WHERE jr.status = 'Pending' AND jr.admin_id = '{admin_id}' AND a.admin_id = '{admin_id}';"""
        logger.debug(f"SQL Query to Fetch Data of Joining Request for Admin : {admin_id} : {sql_query_for_data}" )

        cursor.execute(sql_query_for_data)
        table_data = cursor.fetchall()
        logger.info(f"Data query executed successfully for admin: {admin_id}")
        
        table_columns = ["id","name","emp_type","admin_id","email","mobile","gender","date_of_joining","admin_name"]

        data_formatter = DataFormatter()
        formatted_data = data_formatter.dictionary_list(table_data = table_data,table_column=table_columns)
        logger.info("Data formatted successfully. Ready for sending it to Webpage")
    except Exception as e:
        logger.error(f"Error fetching joining requests: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while rendering joining request page for admin")
    
    else:
        print(formatted_data)
        # return JSONResponse(content = {"message":""})
        logger.info(f"Rendering joining requests page for admin: {admin_id}")
        return templates.TemplateResponse("joining_request.html",context={"request": request ,"data": formatted_data})


@admin_router.post(r"/accept_joining_request", response_class = JSONResponse)
async def accept_joining_request(request : Request, joining_request: AcceptJoiningRequest , db = Depends(get_db)):
    
    """    
    Approval of Joining Request is Processed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        joining_request (AcceptJoiningRequest) : Holds the emp_id and emp_type(Manager/employee).
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"Employee Joining Request was successfully Accepted"}

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """
    
    logger.info(f"Processing acceptance of joining request for ID: {joining_request.id}")
    sql, cursor = db
    if joining_request.emp_type == "Employee":
        query_to_insert_date_in_table = f"""INSERT INTO employees (emp_id,emp_name,password,admin_id,email,mobile,gender,skills)
        SELECT id, name, password, admin_id, email,mobile , gender, 'None'
        FROM joining_request
        WHERE id = '{joining_request.id}';
        """
        logger.debug(f"SQL Query to Insert the data into Employees Table : {query_to_insert_date_in_table}")

    elif joining_request.emp_type == "Manager":
        query_to_insert_date_in_table = f"""INSERT INTO manager (manager_id,manager_name,password,admin_id,email,mobile,gender)
        SELECT id, name, password, admin_id, email, mobile, gender
        FROM joining_request 
        WHERE id = '{joining_request.id}';
        """
        logger.debug(f"SQL Query to Insert the data into Manager Table : {query_to_insert_date_in_table} ")

    
    query_to_update_status_of_joining_request = f"""
    UPDATE joining_request
    SET status = 'Approved'
    WHERE id = '{joining_request.id}' ;
    """
    logger.debug(f"SQL Query to Update the Status column of Joining Request Table : {query_to_update_status_of_joining_request}")

    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(query_to_insert_date_in_table)
        cursor.execute(query_to_update_status_of_joining_request)
        sql.commit()
        logger.info(f"Joining request ID: {joining_request.id} accepted and status updated to 'Approved'")

    except Exception as e:
        sql.rollback()
        logger.error(f"Error while processing acceptance of joining request ID: {joining_request.id} - {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")
    else:
        redirect_url = request.url_for("get_joining_request")
        return JSONResponse(content = {"message":"Employee Joining Request was successfully Accepted"})

@admin_router.post(r"/reject_joining_request", response_class = JSONResponse)
async def reject_joining_request(request : Request, joining_request: RejectJoiningRequest, db = Depends(get_db)) :
    
    """    
    Rejection of Joining Request is Processed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        joining_request (AcceptJoiningRequest) : Holds the emp_id and emp_type(Manager/employee).
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"Employee Joining Request was Rejected"}

    Raises:
        HTTPException [status_code = 500] : error executing query.
    """

    logger.info(f"Processing rejection of joining request for ID: {joining_request.id}")
    sql, cursor = db
    query_to_update_status_of_joining_request = f"""
    UPDATE joining_request
    SET status = 'Rejected'
    WHERE id = '{joining_request.id}' ;
    """
    logger.debug(f"SQL Query to Update the Status column of Joining Request Table : {query_to_update_status_of_joining_request}")

    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(query_to_update_status_of_joining_request)
        sql.commit()
        logger.info(f"Joining request ID: {joining_request.id} rejected and status updated to 'Rejected'")

    except Exception as e:
        sql.rollback()
        logger.error(f"Error while processing rejection of joining request ID: {joining_request.id} - {e}")  
        raise HTTPException(status_code=500, detail="An error occurred while rejecting employee joining request")
    
    else:
        redirect_url = request.url_for("get_joining_request")
        return JSONResponse(content = {"message":"Employee Joining Request was Rejected"})




@admin_router.get(r"/create_project_form", response_class = HTMLResponse)
async def create_project_form(request: Request, admin_id: str = Depends(get_user), db = Depends(get_db)):
    
    """    
    Create Project Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        admin_id (String) : Fetch admin id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] : create_project.html

    Raises:
        HTTPException [status_code = 500] : An error occurred while rendering project form page.
    """

    logger.info(f"{admin_id} : Accessed Project Form Page")
    
    sql, cursor = db
    logger.info(f"Fetching manager details for admin_id: {admin_id}")
    
    sql_query_to_get_manager_detail = f"""SELECT manager_id, manager_name
    FROM manager
    WHERE admin_id = '{admin_id}';"""
    logger.debug(f"SQL Query to fetch Manager details working Under Admin : {admin_id} : {sql_query_to_get_manager_detail} ")

    table_columns = ["admin_id"]
    manager_table_column = ["manager_id","manager_name"]
    try:
        cursor.execute(sql_query_to_get_manager_detail)
        manager_data = cursor.fetchall()
        logger.info(f"Manager details fetched successfully for admin_id: {admin_id}")

        data_formatter = DataFormatter()
        managers = data_formatter.dictionary_list(table_data=manager_data, table_column=manager_table_column)
        logger.info("Data formatted successfully. Ready for sending it to Webpage")
    except Exception as e:
        logger.error(f"Error executing SQL Query or Formatting the Data : {e}")
        raise HTTPException(status_code=500, detail="An error occurred while rendering project form page")
    
    else:
        logger.info(f"Project form was Rendered Successfully")
        return templates.TemplateResponse("create_project.html",{"request":request, "managers":managers, "admin":{"admin_id":admin_id}})



@admin_router.post(r"/create_project_form_processing",response_class=JSONResponse)
async def create_project_form_processing(request: Request, project_details: ProjectDetails, db = Depends(get_db) ):
    
    """    
    Creation of New Project Request is Addressed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        project_details (ProjectDetails) : Fetch user data.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"A Project has been created successfully"}

    Raises:
        HTTPException [status_code = 500] : An error occurred while rendering project form page.
    """

    logger.info(f"Processing project creation for project_id: {project_details.project_id}")
    
    sql, cursor = db
    # status values ["Not Assigned", "Started" , "In Progress" ,"Review" , "On Hold"]

    if project_details.assign_to == "Later" or project_details.assign_to == "later" :
        project_assigned = "NO"
        status_value = "Not Assigned"
    else:
        project_assigned = "YES"
        status_value = "Started"
        
    start_date = datetime.now().strftime('%Y-%m-%d')
    
    sql_query_to_insert_manager_project_details = F"""
        INSERT INTO manager_project_details (manager_id , project_id)
        VALUES ('{project_details.assign_to}','{project_details.project_id}');
        """
    logger.debug(f"SQL Query to insert data into Manager project Detail {sql_query_to_insert_manager_project_details}")

    sql_query_to_create_project = f"""INSERT INTO project (project_id ,project_name, admin_id, start_date, dead_line, status, project_assigned, description)
    VALUES(
        '{project_details.project_id}',
        '{project_details.project_name}', 
        '{project_details.admin_id}',
        '{start_date}',
        '{project_details.dead_line}',
        '{status_value}',
        '{project_assigned}',
        '{project_details.description}'
    );
    """
    print(sql_query_to_create_project)
    logger.debug(f"SQL Query to Create Project {sql_query_to_create_project} ")

    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_create_project)
        if project_assigned == "YES":
            cursor.execute(sql_query_to_insert_manager_project_details)
        sql.commit()
        logger.info(f"Project created successfully with project_id: {project_details.project_id}")

    except Exception as e:
        sql.rollback()
        logger.error(f"error executing above SQL Query or Formatting data: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating new project")
    
    else:
        redirect_url = request.url_for("fetch_all_employees_and_project_for_admin")
        return JSONResponse(content = {"message":"A Project has been created successfully"})

@admin_router.get(r"/admin_view_all",response_class=HTMLResponse)
async def fetch_all_employees_and_project_for_admin(request : Request, admin_id = Depends(get_user),db = Depends(get_db))->None:
    
    """    
    View all Employee and Project Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        admin_id (String): Fetch admin_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] : comprehensive_info.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"{admin_id} : Accessed View all Employee And Project Page")
    logger.info("Fetching all employees, managers, and projects information")
    sql, cursor = db

    sql_query_to_get_all_information = f"""SELECT e.emp_id, e.emp_name, e.gender, e.email,e.admin_id,a.admin_name ,m.manager_id , m.manager_name , p.project_id , p.project_name
    FROM employees AS e
    LEFT JOIN employee_project_details AS epd
    ON e.emp_id = epd.emp_id
    LEFT JOIN project AS p
    ON p.project_id = epd.project_id
    LEFT JOIN manager AS m
    ON m.manager_id = epd.manager_id
    LEFT JOIN admin as a
    ON e.admin_id = a.admin_id
    ORDER BY e.admin_id ASC;
    """
    logger.debug(f"SQL Query to get all Information : {sql_query_to_get_all_information} ")

    sql_query_to_get_manager_information = f"""SELECT m.manager_id, m.manager_name, m.gender, m.email,m.admin_id,a.admin_name , GROUP_CONCAT(mpd.project_id) , GROUP_CONCAT(p.project_name)
    FROM manager AS m
    LEFT JOIN manager_project_details AS mpd
    ON m.manager_id = mpd.manager_id
    LEFT JOIN project AS p
    ON p.project_id = mpd.project_id
    LEFT JOIN admin as a
    ON m.admin_id = a.admin_id
    GROUP BY m.manager_id
    ORDER BY m.admin_id ASC ;"""
    logger.debug(f"SQL Query to get manager Information : {sql_query_to_get_manager_information} ")

    sql_query_to_get_project_information = f"""SELECT p.project_id , p.project_name ,p.admin_id, a.admin_name, p.start_date, p.dead_line, mpd.manager_id, m.manager_name , p.status
    FROM project AS p
    LEFT JOIN manager_project_details AS mpd
    ON mpd.project_id = p.project_id
    LEFT JOIN manager AS m
    ON mpd.manager_id = m.manager_id
    LEFT JOIN admin as a
    ON p.admin_id = a.admin_id
    ORDER BY p.admin_id ASC
    ;
    """
    logger.debug(f"SQL Query to get project Information : {sql_query_to_get_project_information} ")

    table_column_all_information = ["emp_id", "emp_name","gender","email","admin_id","admin_name","manager_id","manager_name","project_id","project_name"]
    table_column_manager_information = ["manager_id", "manager_name","gender","email","admin_id","admin_name","project_id","project_name"]
    table_column_project_information = ["project_id", "project_name","admin_id","admin_name","start_date","dead_line","manager_id","manager_name","status"]
    
    try:
        cursor.execute(sql_query_to_get_all_information)
        table_data_for_worker = cursor.fetchall()
        logger.info(f"All information fetched successfully")

        cursor.execute(sql_query_to_get_manager_information)
        table_data_for_manager = cursor.fetchall()
        logger.info(f"Manager details fetched successfully ")

        cursor.execute(sql_query_to_get_project_information)
        table_data_for_project = cursor.fetchall()
        logger.info(f"Project details fetched successfully")
        logger.info("Successfully fetched all employees, managers, and projects information")

        data_formatter = DataFormatter()
        workers = data_formatter.dictionary_list(table_data = table_data_for_worker, table_column=table_column_all_information)
        managers = data_formatter.dictionary_list(table_data = table_data_for_manager, table_column=table_column_manager_information)
        projects = data_formatter.dictionary_list(table_data = table_data_for_project, table_column=table_column_project_information)
        logger.info("Data formatted successfully. Ready for sending it to Webpage")
    except Exception as e:
        logger.error(f"Error fetching information - {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching information")
    else:
        return templates.TemplateResponse("comprehensive_info.html",{"request":request, "managers": managers,"workers":workers, "projects":projects})

@admin_router.get(r"/admin_view_all_project",response_class=HTMLResponse)
async def fetch_all_project_for_admin(request : Request, admin_id = Depends(get_user),db = Depends(get_db))->None:
    
    """    
    View all  Project Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        admin_id (String): Fetch admin_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] : view_all_project.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"{admin_id} : Accessed View Project Page")
    logger.info("Fetching  projects information")
    sql, cursor = db

    sql_query_to_get_project_information = f"""SELECT p.project_id , p.project_name ,p.admin_id, a.admin_name, p.start_date, p.dead_line, mpd.manager_id, m.manager_name , p.status , p.description
    FROM project AS p
    LEFT JOIN manager_project_details AS mpd
    ON mpd.project_id = p.project_id
    LEFT JOIN manager AS m
    ON mpd.manager_id = m.manager_id
    LEFT JOIN admin as a
    ON p.admin_id = a.admin_id 
    WHERE p.admin_id = '{admin_id}'
    ORDER BY p.admin_id ASC
    ;
    """
    logger.debug(f"SQL Query to get project Information : {sql_query_to_get_project_information} ")

    table_column_project_information = ["project_id", "project_name","admin_id","admin_name","start_date","dead_line","manager_id","manager_name","status","description"]
    
    try:
        cursor.execute(sql_query_to_get_project_information)
        table_data_for_project = cursor.fetchall()
        logger.info(f"Project details fetched successfully")
        logger.info("Successfully fetched all employees, managers, and projects information")

        data_formatter = DataFormatter()
        projects = data_formatter.dictionary_list(table_data = table_data_for_project, table_column=table_column_project_information)
        logger.info("Data formatted successfully. Ready for sending it to Webpage")
    
    except Exception as e:
        logger.error(f"Error fetching information - {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching information")
    
    else:
        return templates.TemplateResponse("view_all_project.html",{"request":request, "projects":projects})


@admin_router.get(r"/assign_project",response_class=HTMLResponse)
async def get_employee_for_assigning_project(request : Request, admin_id: str = Depends(get_user), db = Depends(get_db))->None: 
    
    """    
    Assign project to Manager an Employee Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        admin_id (String): Fetch admin_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] : assign_project.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"{admin_id} : Accessed Assign project to Employee Page")
    logger.info(f"Fetching employees, managers, and projects details for admin_id: {admin_id}")

    sql, cursor = db
    sql_query_to_get_employee_detail = f"""
    SELECT e.emp_id, e.emp_name, e.gender, e.mobile, e.email, e.skills
    FROM employees AS e
    WHERE project_assigned IN ('NO','') AND admin_id = '{admin_id}'; """ 
    logger.debug(f"SQL Query to get Employee Details : {sql_query_to_get_employee_detail} ")

    sql_query_for_project_given_to_employee = f"""SELECT p.project_id, p.project_name 
    FROM project AS p
    INNER JOIN manager_project_details AS mpd
    ON mpd.project_id = p.project_id
    WHERE p.project_assigned = "YES" AND admin_id = '{admin_id}';"""
    logger.debug(f"SQL Query to get Project for Employees : {sql_query_for_project_given_to_employee} ") 

    sql_query_to_get_manager_details = f"""
    SELECT m.manager_id , m.manager_name, m.gender, m.mobile, m.email, 
    GROUP_CONCAT(DISTINCT mpd.project_id ORDER BY mpd.project_id ASC SEPARATOR ', ') AS project_they_have,
    GROUP_CONCAT(DISTINCT p.project_name ORDER BY p.project_id ASC SEPARATOR ', ') AS project_names
    FROM manager AS m
    LEFT JOIN manager_project_details AS mpd
    ON m.manager_id = mpd.manager_id
    LEFT JOIN project AS p
    ON p.project_id = mpd.project_id
    WHERE m.admin_id = '{admin_id}'
    GROUP BY m.manager_id;
    """
    logger.debug(f"SQL Query to get Manager Detail : {sql_query_to_get_manager_details} ")

    sql_query_for_project_given_to_manager = f"""SELECT project_id, project_name 
    FROM project 
    WHERE project_assigned = 'NO' AND admin_id = '{admin_id}' ;""" 
    logger.debug(f"SQL Query to get Project for Manager : {sql_query_for_project_given_to_manager} ") 

    try:
        cursor.execute(sql_query_to_get_employee_detail)
        employee_data = cursor.fetchall()
        logger.info("Fetched employee details successfully")

        cursor.execute(sql_query_to_get_manager_details)
        manager_data = cursor.fetchall()
        logger.info("Fetched manager details successfully")

        cursor.execute(sql_query_for_project_given_to_employee)
        employee_project_options = cursor.fetchall()
        logger.info("Fetched project details for employees successfully")

        cursor.execute(sql_query_for_project_given_to_manager)
        manager_project_options = cursor.fetchall()
        logger.info("Fetched project details for managers successfully")

        employee_table_column = ["emp_id","emp_name","gender","mobile","email","skills"]
        employee_project_column = ["project_id","project_name"]

        manager_table_colum = ["manager_id","manager_name","gender","mobile","email","project_id","project_name"] 
        manager_project_column = ["project_id","project_name"]

        data_formatter = DataFormatter()
        employees = data_formatter.dictionary_list(table_data=employee_data , table_column=employee_table_column)
        employee_projects = data_formatter.dictionary_list(table_data = employee_project_options , table_column = employee_project_column)
        managers = data_formatter.dictionary_list(table_data = manager_data , table_column = manager_table_colum)
        manager_projects = data_formatter.dictionary_list(table_data = manager_project_options , table_column = manager_project_column)
        logger.info("Data formatted successfully for sending it to Webpage")

    except Exception as e:
        logger.error(f"Error fetching or formatting data: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching data")
    
    else:
        logger.error(f"WebPage for assigning project to employees and manager Rendered Successfully") 
        return templates.TemplateResponse("assign_project.html",{"request": request, "employees":employees,"managers":managers,"manager_projects": manager_projects , "employee_projects":employee_projects})


@admin_router.post(r"/assign_employee_a_project",response_class=JSONResponse)
async def assign_project_to_employees(request : Request ,employee_data : AssignProjectToEmployee, db = Depends(get_db) )->None:
    
    """    
    Assigning of project to employee is addressed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        employee_data (AssignProjectToEmployee): Holds project and employee info.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"A project is assigned to employee"}

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"Assigning project_id: {employee_data.project_id} to employee_id: {employee_data.emp_id}")

    sql, cursor = db
    
    sql_query_to_insert_record = f"""
    INSERT INTO employee_project_details (emp_id,manager_id,project_id)
    WITH employee_project_data AS (
    SELECT '{employee_data.emp_id}' AS emp_id, mpd.manager_id AS manager_id ,'{employee_data.project_id}' AS project_id 
    FROM manager_project_details AS mpd
    WHERE mpd.project_id = '{employee_data.project_id}'
    )
    SELECT emp_id , manager_id , project_id FROM employee_project_data ;"""
    logger.debug(f"SQL Query to Save the Record when Project is Assigned to Employee : {sql_query_to_insert_record} ") 


    print(sql_query_to_insert_record)
    sql_query_to_update = f"""UPDATE employees
    SET project_assigned = "YES"
    WHERE emp_id = '{employee_data.emp_id}' ;"""
    logger.debug(f"SQL Query to Update Project Assigned Column in Employees Table : {sql_query_to_update} ") 

    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_insert_record)
        logger.info(f"Successfully Executed the SQL query to Insert the Record in manager_project_detail Table")

        cursor.execute(sql_query_to_update)
        logger.info(f"Successfully Executed the SQL query to Update the project_assign column of Employee Table")

        sql.commit()
        logger.info(f"Successfully assigned project_id: {employee_data.project_id} to employee_id: {employee_data.emp_id}")

    except Exception as e:
        sql.rollback()
        logger.error(f"Error assigning project: {e}")
        HTTPException(status_code = 500, detail = "Error Assigning Project")

    else: 
        redirect_url = request.url_for("get_employee_for_assigning_project")
        return JSONResponse(content = {"message":"A project is assigned to employee"})

@admin_router.post(r"/assign_manager_a_project",response_class=JSONResponse)
async def assign_project_to_employees(request : Request , manager_data: AssignProjectToManager , db = Depends(get_db)):
    
    """    
    Assigning of project to Manager is addressed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        manager_data (AssignProjectToManager): Holds project and manager info.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"A project is assigned to manager"}

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"Assigning project_id: {manager_data.project_id} to manager_id: {manager_data.manager_id}")

    sql,cursor = db
    sql_query_to_find_manager_record = f"""
    SELECT COUNT(project_id) 
    FROM manager_project_details
    WHERE project_id = '{manager_data.project_id}';
    """
    logger.debug(f"SQL Query to find manager record: {sql_query_to_find_manager_record}")

    sql_query_to_update_manager_project_details = f"""
    UPDATE manager_project_details 
    SET manager_id = '{manager_data.manager_id}'
    WHERE project_id = '{manager_data.project_id}';
    """
    logger.debug(f"SQL Query to update manager project details: {sql_query_to_update_manager_project_details}")

    sql_query_to_insert_data = f"""INSERT INTO manager_project_details (manager_id,project_id)
    VALUES('{manager_data.manager_id}','{manager_data.project_id}');
    """
    logger.debug(f"SQL Query to insert data when Manager is Assigned a Project: {sql_query_to_insert_data}")

    sql_query_to_update_project_table = f"""UPDATE project
    SET project_assigned = 'YES', status = 'Started'
    WHERE project_id = '{manager_data.project_id}' ;
    """
    logger.debug(f"SQL Query to update project table: {sql_query_to_update_project_table}")

    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_find_manager_record)
        records = cursor.fetchall()
        logger.info(f"Manager details fetched successfully")

        if records[0][0]:
            cursor.execute(sql_query_to_update_manager_project_details)
            logger.info(f"Manager project details Update successfully ")

        else:
            cursor.execute(sql_query_to_insert_data)
            logger.info(f"Manager project details record saved successfully")

        
        cursor.execute(sql_query_to_update_project_table)
        sql.commit()
        logger.info(f"Successfully assigned project_id: {manager_data.project_id} to manager_id: {manager_data.manager_id}")

    except Exception as e:
        sql.rollback()
        logger.error(f"Error assigning project to manager: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while assigning the project to the manager")
   
    else: 
        redirect_url = request.url_for("get_employee_for_assigning_project")
        return JSONResponse(content = {"message":"A project is assigned to manager"})



@admin_router.get(r"/unassign_project",response_class=HTMLResponse)
async def unassign_project_page(request : Request, admin_id: str = Depends(get_user), db = Depends(get_db))->None:
    
    """    
    Unassign Manager and Employee from Project Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        admin_id (String): Fetch admin_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] : unassign_project.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"{admin_id} : Accessed Unassign Project to Employee Page")
    logger.info(f"Fetching employee and manager project details for admin_id: {admin_id}")

    sql, cursor = db
    sql_query_to_find_employee_project = f"""SELECT e.emp_id,e.emp_name, e.gender , e.mobile , e.email,
    p.project_id , p.project_name, m.manager_id , m.manager_name
    FROM employees AS e
    INNER JOIN employee_project_details AS epd
    ON e.emp_id = epd.emp_id 
    INNER JOIN project AS p
    ON p.project_id = epd.project_id
    INNER JOIN manager  AS m
    ON m.manager_id = epd.manager_id
    WHERE e.admin_id = '{admin_id}'
    ;
    """
    logger.debug(f"SQL Query to find employee project: {sql_query_to_find_employee_project}")

    sql_query_to_find_manager_project = f"""SELECT m.manager_id , m.manager_name , m.gender , m.mobile , m.email,
    GROUP_CONCAT(DISTINCT p.project_id ORDER BY p.project_id ASC SEPARATOR ', ') AS project_id,
    GROUP_CONCAT(DISTINCT p.project_name ORDER BY p.project_id ASC SEPARATOR ', ') AS project_name
    FROM manager_project_details AS mpd
    INNER JOIN manager AS m
    ON m.manager_id = mpd.manager_id
    INNER JOIN project AS p
    ON p.project_id = mpd.project_id
    WHERE m.admin_id = '{admin_id}' 
    GROUP BY m.manager_id ;"""
    logger.debug(f"SQL Query to find manager project: {sql_query_to_find_manager_project}")

    employee_table_column = ["emp_id","emp_name","gender","mobile","email","project_id", "project_name","manager_id","manager_name"]
    manager_table_column = ["manager_id", "manager_name","gender","mobile","email","project_id","project_name"]

    try:
        cursor.execute(sql_query_to_find_employee_project)
        employee_data = cursor.fetchall()
        logger.info("Fetched employee project details successfully")

        cursor.execute(sql_query_to_find_manager_project)
        manager_data = cursor.fetchall()
        logger.info("Fetched manager project details successfully")

        data_formatter = DataFormatter()
        employees = data_formatter.dictionary_list(table_data = employee_data, table_column=employee_table_column)
        managers = data_formatter.dictionary_list(table_data = manager_data, table_column=manager_table_column)
        logger.info("Data formatted successfully. Ready for sending it to Webpage")

    except Exception as e:
        logger.error(f"Error fetching or formatting data: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching data")
   
    else:
        logger.info("Successfully Rendered the Unassign Project Webpage")
        return templates.TemplateResponse("unassign_project.html",{"request":request,"employees":employees,"managers":managers})

@admin_router.put(r"/unassign_employee_from_project",response_class=JSONResponse)
async def unassig_employee_from_project(request : Request, employee_data : UnassignProjectToEmployee, db = Depends(get_db)  )->None:

    """    
    Unassign Employee from Project Resquest is Processed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        employee_data (UnassignProjectToEmployee): Fetch Data of User and Project.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"Employee was unassigned from a Project"}

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"Unassigning employee {employee_data.emp_id} from project")
    sql, cursor = db
    sql_query_to_unassign_employee_from_project = f"""
    DELETE FROM employee_project_details
    WHERE emp_id = '{employee_data.emp_id}' ;
    """
    logger.debug(f"SQL Query to Delete Employee Record from employee_project_detail Table: {sql_query_to_unassign_employee_from_project}")


    sql_query_to_update_employee_table = f"""UPDATE employees
    SET project_assigned = 'NO'
    WHERE emp_id = '{employee_data.emp_id}' ;"""
    logger.debug(f"SQL Query to Update Project_Assigned Column from employees Table: {sql_query_to_update_employee_table}")

    
    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_unassign_employee_from_project)
        cursor.execute(sql_query_to_update_employee_table)
        sql.commit()
        logger.info(f"Employee {employee_data.emp_id} successfully unassigned from project and Employee Table Update")

    except Exception as e:
        sql.rollback()
        logger.error(f"Error unassigning employee from project: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while unassigning the employee")

    else:
        redirect_url = request.url_for("unassign_project_page")
        return JSONResponse(content = {"message":"Employee was unassigned from a Project"})

@admin_router.put(r"/unassign_manager_from_project",response_class=JSONResponse)
async def unassig_manager_from_project(request : Request, manager_data: UnassignProjectToManager, db = Depends(get_db) )->None:

    """    
    Unassign Manager from Project Resquest is Processed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        manager_data (UnassignProjectToManager): Fetch Data of User and Project.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"Manager was unassigned from a Project"}

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"Unassigning manager {manager_data.manager_id} from project {manager_data.project_id}")
    sql, cursor = db
    sql_query_to_update_manager_project_details =  f"""
    UPDATE manager_project_details
    SET manager_id = 'Unassigned'
    WHERE manager_id = '{manager_data.manager_id}' AND project_id = '{manager_data.project_id}' ;
    """
    logger.debug(f"SQL Query to Update the Manager_project_detail Table : {sql_query_to_update_manager_project_details} ") 

    sql_query_to_update_project = f"""UPDATE project
    SET project_assigned = 'NO',
    status = 'On Hold'
    WHERE project_id = '{manager_data.project_id}'; """
    logger.debug(f"SQL Query to Update Project Status in Project Table : {sql_query_to_update_project} ") 


    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_update_manager_project_details)
        cursor.execute(sql_query_to_update_project)
        sql.commit()
        logger.info(f"Manager {manager_data.manager_id} successfully unassigned from project {manager_data.project_id}")
        
    except Exception as e:
        sql.rollback()
        logger.error(f"Error unassigning manager from project: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while unassigning the manager")
    else:
        redirect_url = request.url_for("unassign_project_page")
        return JSONResponse(content = {"message":"Manager was unassigned from a Project"})

@admin_router.get(r"/manager_request",response_class=HTMLResponse)
async def get_manager_request(request : Request, admin_id: str = Depends(get_user), db = Depends(get_db)):

    """    
    Manager Request for Employee Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        admin_id (String): Fetch admin_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] : manager_request.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"{admin_id} : Accessed Manager Request Page")
    logger.info(f"Fetching manager requests for admin_id: {admin_id}")
    sql, cursor = db
    sql_query_for_manager_request = f"""
    SELECT m.manager_name, m.manager_id, p.project_name , p.project_id , e.emp_name , e.emp_id
    FROM manager_request_for_employees AS mrfe
    INNER JOIN manager AS m
    ON mrfe.manager_id = m.manager_id
    INNER JOIN project AS p
    ON mrfe.project_id = p.project_id
    INNER JOIN employees AS e
    ON mrfe.emp_id = e.emp_id
    WHERE mrfe.status = "Pending" AND mrfe.admin_id = '{admin_id}'
    GROUP BY m.manager_id, p.project_id,e.emp_id;
    """
    logger.debug(f"SQL Query to fetch Manager Request : {sql_query_for_manager_request} ") 
    table_column = ["manager_name", "manager_id","project_name","project_id","emp_name","emp_id"]
    try:
        cursor.execute(sql_query_for_manager_request)
        data = cursor.fetchall()
        logger.info("Fetched manager requests successfully")

        data_formatter = DataFormatter()
        data_entries = data_formatter.dictionary_list(table_data=data, table_column=table_column)
        logger.info("Data formatted successfully. Ready for sending it to Webpage")

    except Exception as e:
        logger.error(f"Error fetching manager requests: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching manager requests")
    
    else: 
        return templates.TemplateResponse("manager_request.html",{"request":request,"data_entries":data_entries})

@admin_router.post(r"/accept_manager_request",response_class=JSONResponse)
async def accept_manager_request(request : Request, manager_request_for_employees: ManagerRequestForEmployees, db = Depends(get_db)):

    """    
    Approval  Manager Request is Processed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        manager_request_for_employee (ManagerRequestForEmployee): Holds employee and manager info.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"Manager request Accepted"}

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"Accepting manager request for employee {manager_request_for_employees.emp_id} for project {manager_request_for_employees.project_id} assigned by manager {manager_request_for_employees.manager_id}")

    sql, cursor = db
    sql_query_to_insert_record = f"""
    INSERT INTO employee_project_details (emp_id,project_id,manager_id)
    VALUES ('{manager_request_for_employees.emp_id}', '{manager_request_for_employees.project_id}', '{manager_request_for_employees.manager_id}')"""
    logger.debug(f"[Query 1]: SQL Query to save Record when manager request is Accepted : {sql_query_to_insert_record} ") 

    sql_query_to_update = f"""
    UPDATE manager_request_for_employees
    SET status = 'Approved'
    WHERE emp_id = '{manager_request_for_employees.emp_id}' AND project_id = '{manager_request_for_employees.project_id}' AND manager_id = '{manager_request_for_employees.manager_id}';
    """
    logger.debug(f"[Query 2]: SQL Query to Update the status of Manager Request : {sql_query_to_update} ") 


    sql_query_to_update_employee_record = f"""
    UPDATE employees
    SET project_assigned = 'YES'
    WHERE emp_id = '{manager_request_for_employees.emp_id}';"""
    logger.debug(f"[Query 3]: SQL Query to Update the project_assigned column of employees : {sql_query_to_update_employee_record} ") 


    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_insert_record)
        logger.info("Query 1 Successfully Executed")

        cursor.execute(sql_query_to_update_employee_record)
        logger.info("Query 2 Successfully Executed")

        cursor.execute(sql_query_to_update)
        logger.info("Query 3 Successfully Executed")

        sql.commit()
        logger.info(f"Manager request for employee {manager_request_for_employees.emp_id} accepted successfully")

    except Exception as e:
        sql.rollback()
        logger.error(f"Error accepting manager request: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while accepting the manager request")
    
    else: 
        redirect_url = request.url_for('get_manager_request')
        return JSONResponse(content = {"message":"Manager request Accepted"})
    
@admin_router.put(r"/reject_manager_request",response_class=JSONResponse)
async def reject_manager_request(request : Request, manager_request_for_employees: ManagerRequestForEmployees, db = Depends(get_db)):

    """    
    Rejection of Manager Request for Employee is Processed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        manager_request_for_employees (ManagerRequestForEmployees): Fetch Data of User and Project.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"Manager request Rejected"}
        
    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"Rejecting manager request for employee {manager_request_for_employees.emp_id} for project {manager_request_for_employees.project_id} assigned by manager {manager_request_for_employees.manager_id}")
    sql, cursor = db
    sql_query_to_update_manager_request_status = f"""
    UPDATE manager_request_for_employees
    SET status = 'Rejected'
    WHERE emp_id = '{manager_request_for_employees.emp_id}' AND project_id = '{manager_request_for_employees.project_id}' AND manager_id = '{manager_request_for_employees.manager_id}';
    """
    logger.debug(f"SQL Query to Update status of Manager Request When it is Rejected : {sql_query_to_update_manager_request_status} ") 

    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_update_manager_request_status)
        sql.commit()
        logger.info(f"Manager request for employee {manager_request_for_employees.emp_id} rejected successfully")
   
    except Exception as e:
        sql.rollback()
        logger.error(f"Error rejecting manager request: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while rejecting the manager request")
    
    else: 
        redirect_url = request.url_for('get_manager_request')
        return JSONResponse(content = {"message":"Manager request Rejected"})

#[In Progress]
@admin_router.get(r"/update_employee_skill",response_class=HTMLResponse)
async def update_employees_skill(request : Request, admin_id: str = Depends(get_user), db = Depends(get_db)) :

    """    
    Update Employee Skill Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        admin_id (String): Fetch admin_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] : update_skill.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"{admin_id} : Accessed Update Skill of Employee Page")
    logger.info(f"Fetching employee details for admin {admin_id} to update skills")
    sql, cursor = db
    sql_query_to_get_employee_details = f"""SELECT e.emp_id, e.emp_name, e.gender, e.mobile, e.email, e.skills
    FROM employees AS e
    WHERE admin_id = '{admin_id}'; """
    logger.debug(f"SQL Query to fetch Employees Details : {sql_query_to_get_employee_details} ") 

    try:
        cursor.execute(sql_query_to_get_employee_details)
        employee_data = cursor.fetchall()
        logger.info(f"Fetched employee details successfully for admin {admin_id}")

        employee_table_column = ["emp_id","emp_name","gender","mobile","email","skills"]

        data_formatter = DataFormatter()
        employees = data_formatter.dictionary_list(table_data=employee_data,table_column=employee_table_column)
        logger.info("Data formatted successfully. Ready for sending it to Webpage")

    except Exception as e:
        logger.error(f"Error fetching employee details: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching employee details")
    
    else:
        return templates.TemplateResponse("update_skill.html",{"request": request,"employees":employees}) 

@admin_router.put(r"/add_employee_skill",response_class=JSONResponse)
async def update_employees_skill(request : Request, employee_data: UpdateSkill, db = Depends(get_db)) :

    """    
    Add Employee Skill Request is Processed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        employee_data (UpdateSkill): Fetch skill to be add and emp_id.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"skill added successfully"}
        
    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"Adding skill '{employee_data.skills}' to employee with ID: {employee_data.emp_id}")
    
    sql, cursor = db
    sql_query_to_add_skill = f"""
    UPDATE employees
    SET skills = CONCAT(skills,' {employee_data.skills}')
    WHERE emp_id = '{employee_data.emp_id}';
    """
    logger.debug(f"SQL Query to add Employee Skill : {sql_query_to_add_skill} ") 

    print(sql_query_to_add_skill)
    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_add_skill)
        sql.commit()
        logger.info("Skill added successfully")

    except Exception as e:
        sql.rollback()
        logger.error(f"Error adding skill: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while adding skill")
    
    else:
        
        redirect_url = request.url_for("update_employees_skill")
        return JSONResponse(content = {"message":"skill added successfully"})

@admin_router.put(r"/replace_employee_skill",response_class=JSONResponse)
async def update_employees_skill(request : Request, employee_data: UpdateSkill, db = Depends(get_db)) :

    """    
    Replace Employee Skill Request is Processed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        employee_data (UpdateSkill): Fetch skill to be replaced and emp_id.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"Employee skill replaced Successfully"}
        
    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"Replacing skill for employee with ID: {employee_data.emp_id} with '{employee_data.skills}'")
    
    sql, cursor = db
    sql_query_to_replace_skill = f"""
    UPDATE employees
    SET skills =  '{employee_data.skills}'
    WHERE emp_id = '{employee_data.emp_id}';
    """
    logger.debug(f"SQL Query to Replace Employee Skill : {sql_query_to_replace_skill} ") 

    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_replace_skill)
        sql.commit()
        logger.info("Employee skill replaced successfully")

    except Exception as e:
        sql.rollback()
        logger.error(f"Error replacing skill: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while replacing skill")
   
    else:
        redirect_url = request.url_for("update_employees_skill")
        return JSONResponse(content = {"message":"Employee skill replaced Successfully"})

@admin_router.get(r"/manager_request_to_complete_project",response_class=HTMLResponse)
async def manager_request_to_complete_project_page(request : Request, admin_id: str = Depends(get_user), db = Depends(get_db)):

    """    
    Manager Request for Completion of Project Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        admin_id (String): Fetch admin_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] : manager_request_to_complete_project.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"{admin_id} : Accessed View completed Project Page")
    logger.info("Fetching project information")
    sql, cursor = db

    
    sql_query_to_get_project_information = f"""SELECT p.project_id , p.project_name ,p.admin_id, a.admin_name, p.start_date, p.dead_line, mpd.manager_id, m.manager_name , p.status
    FROM project AS p
    LEFT JOIN manager_project_details AS mpd
    ON mpd.project_id = p.project_id
    LEFT JOIN manager AS m
    ON mpd.manager_id = m.manager_id
    LEFT JOIN admin as a
    ON p.admin_id = a.admin_id
    WHERE p.status = 'completed'
    ORDER BY p.admin_id ASC
    ;
    """
    logger.debug(f"SQL Query to get project Information : {sql_query_to_get_project_information} ")

    table_column_project_information = ["project_id", "project_name","admin_id","admin_name","start_date","dead_line","manager_id","manager_name","status"]
    
    try:
        cursor.execute(sql_query_to_get_project_information)
        table_data_for_project = cursor.fetchall()
        logger.info(f"Project details fetched successfully")

        data_formatter = DataFormatter()
        projects = data_formatter.dictionary_list(table_data = table_data_for_project, table_column=table_column_project_information)
        logger.info("Data formatted successfully. Ready for sending it to Webpage")
    except Exception as e:
        logger.error(f"Error fetching information - {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching information")
    else:
        return templates.TemplateResponse("manager_request_to_complete_project.html",{"request":request,  "projects":projects})

@admin_router.put("/reject_completion_of_project")
async def reject_completion_of_project(request : Request, project_id :str, db = Depends(get_db)):

    """    
    Rejection of Manager Request of completion of project is Processed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        project_id (String): Holds Project_id.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"Employee skill replaced Successfully"}
        
    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"Processing rejection of completion of project: {project_id}")
    sql, cursor = db
    query_to_update_status_of_project = f"""
    UPDATE project
    SET status = 'Review'
    WHERE project_id = '{project_id}' ;
    """
    logger.debug(f"SQL Query to Update the Status column of Project Table : {query_to_update_status_of_project}")

    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(query_to_update_status_of_project)
        sql.commit()
        logger.info(f"project ID: {project_id}  status updated to 'Review'")

    except Exception as e:
        sql.rollback()
        logger.error(f"Error while Updating project status of  ID: {project_id} - {e}")  
        raise HTTPException(status_code=500, detail="An error occurred while rejecting completion of project")
    
    else:
        return JSONResponse(content = {"message":"Project status set to Review"})


@admin_router.delete("/approve_completion_of_project")
async def approve_completion_of_project(request : Request, project_id :str, db = Depends(get_db)):

    """    
    Approval of completion of project is Processed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        project_id (String): Holds project_id.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"Project Completed"}
        
    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"Processing Approval of completion of project: {project_id}")
    sql, cursor = db
    sql_query_to_update_employee_table = f"""
    UPDATE employees
    SET project_assigned = 'NO'
    WHERE emp_id IN (SELECT emp_id FROM employee_project_details WHERE project_id = '{project_id}');
    """
    logger.debug(f"SQL Query to free the employee from project : {sql_query_to_update_employee_table}")

    sql_query_to_save_project = f"""INSERT INTO project_completed(project_id,project_name, admin_id,admin_name, start_date, dead_line, status, description , project_completion_date)
    SELECT p.project_id , p.project_name, p.admin_id , a.admin_name , p.start_date, p.dead_line, p.status, p.description , CURDATE()
    FROM project AS p , admin AS a
    WHERE project_id = '{project_id}' AND a.admin_id = p.admin_id;"""
    logger.debug(f"SQL Query to Save Project Completed : {sql_query_to_save_project}")

    query_to_delete_project = f"""
    DELETE FROM project WHERE project_id = '{project_id}';
    """
    logger.debug(f"SQL Query to delete Project Completed : {query_to_delete_project}")

    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_update_employee_table)
        cursor.execute(sql_query_to_save_project)
        cursor.execute(query_to_delete_project)
        sql.commit()
        logger.info(f"project ID: {project_id} status was changed to completed. ")

    except Exception as e:
        sql.rollback()
        logger.error(f"Error while Updating project status of  ID: {project_id} - {e}")  
        raise HTTPException(status_code=500, detail="An error occurred while approving project completion")
    
    else:
        return JSONResponse(content = {"message":"Project Completed"})



@admin_router.get(r"/remove_workers",response_class=HTMLResponse)
async def remove_employees_page(request : Request, admin_id: str = Depends(get_user), db = Depends(get_db)):

    """    
    Remove Employee Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        admin_id (String): Fetch admin_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] :remove_employee.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"{admin_id} : Accessed Remove Employee Page Page")
    logger.info(f"Fetching managers and employees data for admin {admin_id} to remove workers")
    
    sql, cursor = db
    query_for_manager = f"""
    SELECT manager_name, manager_id, email,mobile , gender
    FROM manager
    WHERE admin_id = '{admin_id}'"""
    logger.debug(f"SQL Query to Fetch Manager Details : {query_for_manager} ") 

    query_for_employee = f"""
    SELECT emp_name, emp_id, email,mobile , gender
    FROM employees
    WHERE admin_id = '{admin_id}'"""
    logger.debug(f"SQL Query to Fetch Employee Detail : {query_for_employee} ") 


    table_column = ["name","id","email","mobile","gender"]
    try:
        print(admin_id)
        cursor.execute(query_for_manager)
        manager_data = cursor.fetchall()
        logger.info("Fetched managers data successfully")

        cursor.execute(query_for_employee)
        employee_data = cursor.fetchall()
        logger.info("Fetched managers data successfully")

        data_formatter = DataFormatter()
        manager_data_entries = data_formatter.dictionary_list(table_data=manager_data, table_column=table_column)
        employees_data_entries = data_formatter.dictionary_list(table_data=employee_data, table_column=table_column)
        logger.info("Data formatted successfully. Ready for sending it to Webpage")
    except Exception as e:
        logger.error(f"Error fetching managers and employees data: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching data")
   
    else:
        return templates.TemplateResponse("remove_employee.html",{"request":request,"managers":manager_data_entries,"employees":employees_data_entries})


#[In Progress]
@admin_router.delete("/remove_manager",response_class=JSONResponse)
async def remove_manager(request : Request , manager_id : str, db = Depends(get_db)):

    """    
    Removal of Manager is Processed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        manager_id (String): Holds manager_id.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"Manager has been removed successfully"}
        
    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"Removing manager with ID: {manager_id}")
    sql, cursor = db
    sql_query_to_store_record = f"""
    INSERT INTO employee_termination_records (id,name,emp_type,admin_id,admin_name,email,mobile,gender,date_of_joining,departure_date)
    WITH manager_data AS(
        SELECT m.manager_id , m.manager_name ,'Manager', m.admin_id , a.admin_name , m.email , m.mobile , m.gender , jr.date_of_joining, CURDATE()
        FROM manager AS m
        INNER JOIN admin AS a
        ON a.admin_id = m.admin_id
        INNER JOIN joining_request AS jr
        ON m.manager_id = jr.id AND m.admin_id = jr.admin_id
        WHERE m.manager_id = '{manager_id}'
    )
    SELECT * FROM manager_data;
    """
    logger.debug(f"[Query 1]: SQL Query to save Record of Terminated Manager : {sql_query_to_store_record} ") 

    sql_query_to_remove_manager = f"""
    DELETE FROM manager
    WHERE manager_id = '{manager_id}' ;
    """
    logger.debug(f"[Query 2]: SQL Query to Remove Manager : {sql_query_to_remove_manager} ")

    sql_query_for_updating = f"""UPDATE manager_project_details
    set manager_id = 'Terminated'
    WHERE manager_id = '{manager_id}';
    """
    logger.debug(f"[Query 3]: SQL Query to Update the Project Incharge : {sql_query_for_updating} ")

    sql_query_to_update_project = f"""UPDATE project
    SET project_assigned = 'NO'
    WHERE project_id in (
        SELECT project_id FROM manager_project_details WHERE manager_id = '{manager_id}'
        );
    """ 
    logger.debug(f"[Query 4]: SQL Query to save Update Project Status : {sql_query_to_update_project} ")

    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_store_record)
        logger.info("Query 1 Successfully Executed")

        cursor.execute(sql_query_to_update_project)
        logger.info("Query 2 Successfully Executed")

        cursor.execute(sql_query_for_updating)
        logger.info("Query 3 Successfully Executed")

        cursor.execute(sql_query_to_remove_manager)
        logger.info("Query 4 Successfully Executed")

        sql.commit()
        logger.info("Manager removed successfully")

    except Exception as e:
        sql.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while removing Manager")
    
    else:
        
        redirect_url = request.url_for('remove_employees_page')
        return JSONResponse(content = {"message":"Manager has been removed successfully"})
    

@admin_router.delete("/remove_employee", response_class=JSONResponse)
async def remove_employee(request : Request , emp_id: str, db = Depends(get_db)):

    """    
    Removal of Employee is Processed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        emp_id (String): Holds emp_id.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json : {"message":"Employee has been removed successfully"}
        
    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"Removing employee with ID: {emp_id}")
    sql, cursor = db
    sql_query_to_remove_employee = f"""
    DELETE FROM employees
    WHERE emp_id = '{emp_id}' ;
    """
    logger.debug(f"[Query 1]: SQL Query to Remove Employee : {sql_query_to_remove_employee} ")

    sql_query_to_store_record = f"""
    INSERT INTO employee_termination_records (id,name,emp_type,admin_id,admin_name,email,mobile,gender,date_of_joining,departure_date)
    WITH manager_data AS(
        SELECT e.emp_id , e.emp_name ,'Employee', e.admin_id , a.admin_name , e.email , e.mobile , e.gender , jr.date_of_joining, CURDATE()
        FROM employees AS e
        INNER JOIN admin AS a
        ON a.admin_id = e.admin_id
        INNER JOIN joining_request AS jr
        ON e.emp_id = jr.id AND e.admin_id = jr.admin_id
        WHERE e.emp_id = '{emp_id}'
    )
    SELECT * FROM manager_data;
    """
    logger.debug(f"[Query 2]: SQL Query to save Record of Terminated Employee : {sql_query_to_store_record} ")

    print(sql_query_to_remove_employee)
    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_store_record)
        logger.info("Query 1 Successfully Executed")

        cursor.execute(sql_query_to_remove_employee)
        logger.info("Query 2 Successfully Executed")
        
        sql.commit()
        logger.info("Employee removed successfully")

    except Exception as e:
        sql.rollback()
        logger.error(f"Error removing employee: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while removing employee")
    
    else:
        
        redirect_url = request.url_for('remove_employees_page')
        return JSONResponse(content={"message":"Employee has been removed successfully"})
    
    
@admin_router.post("/admin_logout",response_class = HTMLResponse)
async def logout(request: Request):
    logger.info("Admin successfully logged out")
    admin_user.logout()
    return JSONResponse(content = {"message": "Admin successfully Logout"})


'''
The below code is only used in Testing.

Remove all the test entity [project | Manager | Employee] I created while testing.
'''

@admin_router.delete("/remove_all",response_class= JSONResponse)
async def remove_all(request:Request , admin_id: str, db = Depends(get_db) ):
    logger.info(f"Removing all data for admin ID: {admin_id}")
    sql, cursor = db

    sql_query_to_remove_employee = f"""DELETE FROM employees
    WHERE admin_id REGEXP '^Test' ;"""
    sql_query_to_remove_manager = f"""DELETE FROM manager
    WHERE admin_id REGEXP '^Test' ;"""
    sql_query_to_remove_project = f"""DELETE FROM project
    WHERE admin_id REGEXP '^Test' ;"""
    sql_query_to_remove_joining_request = f"""DELETE FROM joining_request
    WHERE admin_id REGEXP '^Test' ;"""
    sql_query_to_remove_terminated_records = f"""DELETE FROM employee_termination_records
    WHERE admin_id REGEXP '^Test' ;"""

    sql_query_to_remove_test_project_records = f"""DELETE FROM project_completed
    WHERE admin_id REGEXP '^Test' ;"""
    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_remove_employee)
        cursor.execute(sql_query_to_remove_manager)
        cursor.execute(sql_query_to_remove_project)
        cursor.execute(sql_query_to_remove_joining_request)
        cursor.execute(sql_query_to_remove_terminated_records)
        cursor.execute(sql_query_to_remove_project)
        cursor.execute(sql_query_to_remove_test_project_records)
        sql.commit()
        logger.info("All data removed successfully")

    except Exception as e:
        sql.rollback()
        logger.error("error occured while removing all data")
        raise HTTPException(status_code=500, detail="An error occurred while removing all data")
    
    else:
        return JSONResponse(content = {"message":"Everything Removed Successfully"})
    