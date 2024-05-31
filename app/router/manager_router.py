"""
To use, simply 'import manager_router'

This module holds all the functionalities that a manager has.
1. Manager Login Panal
2. View all employee and project
3. Filter employee (unassigned) on the basis of skill
4. Request admin for employee for project
5. View project he/she has
6. Update the status of project
7. Logout
""" 

from fastapi import APIRouter, HTTPException , Request , status, Depends , Response 
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse , RedirectResponse, JSONResponse
from models.employee_model import RequestForEmployee
from models.index_model import LoginDetails
from models.project_model import Project_Update_Status
from config.db_connection import get_db
from schema.schemas import DataFormatter
import logging 
from logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
class ManagerUserSession:
    def __init__(self):
        self.manager_id = None
    
    def login(self, username):
        self.manager_id = username
    
    def logout(self):
        self.manager_id = None
    
    def is_authenticated(self):
        return self.manager_id is not None

manager_user = ManagerUserSession()
def get_user():
    if manager_user.manager_id:
        return manager_user.manager_id
    else:
        raise HTTPException(status_code=401, detail="Unauthoroised User")
manager_router = APIRouter()


templates = Jinja2Templates(directory = "templates/manager")
@manager_router.get("/manager_login")
async def manager_login(request: Request):

    """    
    Manager Login Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        
    Returns:
        [text/html] :index.html

    """

    logger.info(f"Accessed Manager Login Page")
    return templates.TemplateResponse("index.html",{"request":request}) 

@manager_router.post(r"/manager_login_data", response_class = HTMLResponse)
async def manager_credential_authentication(response: Response,request : Request, login_details: LoginDetails, db = Depends(get_db)) -> None:
    
    """    
    Manager Credential will be Authenticated here.

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
    sql , cursor = db

    sql_query_to_check_manager = f"""SELECT COUNT(manager_id) ,manager_id, password 
    FROM manager
    WHERE manager_id = '{login_details.username}' AND password = '{login_details.password}' ;
    """
    logger.debug(f"SQL Query to Check Wheather Manager Record Exist or Not : {sql_query_to_check_manager}")

    print( "manager",login_details.username , login_details.password )

    try:
        cursor.execute(sql_query_to_check_manager)
        data = cursor.fetchall()
        logger.info(f"Authentication query executed successfully for admin: {login_details.username}")

    except Exception as e:
        logger.error(f"Error executing authentication query: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while executing authentication query")
    
    else:
        condition = data[0][0]
        print(type(condition))
 
        if condition:
            logger.info(f"Employee {login_details.username} authenticated successfully.")

            manager_user.login(login_details.username)
            logger.info("Employee id is saved as SessionUser")
            logger.info(f"Redirecting to Employee home ")

            redirect_url = request.url_for('admin_home')
            print(redirect_url)
            return JSONResponse(content={"message":"Login Successful"})
        
        else:
            logger.warning(f"Invalid login attempt for admin: {login_details.username}")
            raise HTTPException(status_code=401, detail="Invalid username or password")

      

@manager_router.get("/manager_home")
async def manager_home(request: Request, manager_id = Depends(get_user)):
    
    """    
    Manager Home Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        manager_id (String): Fetch manager_id from UserSession.
        
    Returns:
        [text/html] :home.html
    """

    logger.info(f"{manager_id} : Accessed Manager Home Page")
    return templates.TemplateResponse("home.html",{"request":request}) 


@manager_router.get(r"/comprehensive_info")
async def get_all_employees_and_project(request: Request,manager_id = Depends(get_user), db = Depends(get_db)) -> None:
    
    """    
    View all Employee and Project Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        manager_id (String): Fetch manager_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] :compresive_info.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"{manager_id} : Accessed View all Employees Page")

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
    ON a.admin_id = e.admin_id
    ORDER BY a.admin_id ASC;"""
    logger.debug(f"[Query 1] : SQL Query to Fetch all the Employees Information")

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

    sql_query_to_get_project_information = f"""SELECT p.project_id , p.project_name , a.admin_id , a.admin_name,p.start_date, p.dead_line, mpd.manager_id, m.manager_name 
    FROM project AS p
    LEFT JOIN manager_project_details AS mpd
    ON mpd.project_id = p.project_id
    LEFT JOIN manager AS m
    ON mpd.manager_id = m.manager_id
    LEFT JOIN admin AS a
    ON a.admin_id = p.admin_id
    ;
    """
    logger.debug(f"[Query 3] : SQL Query to Fetch all the projects Information")

    table_column_all_information = ["emp_id", "emp_name","gender","email","admin_id","admin_name","manager_id","manager_name","project_id","project_name"]
    table_column_manager_information = ["manager_id", "manager_name","gender","email","admin_id","admin_name","project_id","project_name"]
    table_column_project_information = ["project_id", "project_name","admin_id","admin_name","start_date","dead_line","manager_id","manager_name"]
    
    try:
        cursor.execute(sql_query_to_get_all_information)
        table_data_for_worker = cursor.fetchall()
        logger.info(f"Query 1 Executed and Fetched Data Successfully")

        cursor.execute(sql_query_to_get_manager_information)
        table_data_for_manager = cursor.fetchall()
        logger.info(f"Query 2 Executed and Fetched Data Successfully")

        cursor.execute(sql_query_to_get_project_information)
        table_data_for_project = cursor.fetchall()
        logger.info(f"Query 3 Executed and Fetched Data Successfully")

        data_formatter = DataFormatter()
        workers = data_formatter.dictionary_list(table_data = table_data_for_worker, table_column=table_column_all_information)
        managers = data_formatter.dictionary_list(table_data = table_data_for_manager, table_column=table_column_manager_information)
        projects = data_formatter.dictionary_list(table_data = table_data_for_project, table_column=table_column_project_information)
        logger.info("Data formatted successfully. Ready for sending it to Webpage")
    
    except Exception as e:
        logger.error(f"Error executing query or while formatting the Data: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while view all employee page")
    
    else:
        return templates.TemplateResponse("comprehensive_info.html",{"request":request, "managers": managers,"workers":workers, "projects":projects})


@manager_router.get(r"/filtered_employee")
async def get_filtered_employees(request: Request, skill:str = "" , manager_id: str = Depends(get_user), db = Depends(get_db) ) -> None:
    
    """    
    Employee (Unassigned) for Project Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        skill (String) : Hold value of filter.
        manager_id (String): Fetch manager_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] :filter_employee_for_project.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"{manager_id} : Accessed Employee for Project Page")
    sql , cursor = db
    sql_query_to_fetch_employees = f"""SELECT e.emp_id , e.emp_name , e.gender , e.mobile , e.email , e.skills
    FROM employees AS e,manager AS m
    WHERE m.manager_id = '{manager_id}' AND e.admin_id = m.admin_id AND e.project_assigned = 'NO' AND e.skills REGEXP '{skill}';
    """
    logger.debug(f"[Query 1] : SQL Query to Fetch Unassigned Employee Information")

    sql_query_to_fetch_projects = f"""SELECT mpd.project_id , p.project_name
    FROM manager_project_details AS mpd
    INNER JOIN project AS p
    ON p.project_id = mpd.project_id
    WHERE mpd.manager_id = '{manager_id}';
    """
    logger.debug(f"[Query 2] : SQL Query to Fetch all the projects Information which is Under {manager_id}")



    table_column_employee_information = ["emp_id", "emp_name","gender","mobile","email","skills"]
    project_column = ["project_id","project_name"]
    
    try:
        cursor.execute(sql_query_to_fetch_employees)
        table_data_for_employee_request = cursor.fetchall()
        logger.info(f"Query 1 Executed and Fetched Data Successfully")

        cursor.execute(sql_query_to_fetch_projects)
        data_of_project = cursor.fetchall()
        logger.info(f"Query 2 Executed and Fetched Data Successfully")

        data_formatter = DataFormatter()
        workers = data_formatter.dictionary_list(table_data = table_data_for_employee_request, table_column=table_column_employee_information)
        projects = data_formatter.dictionary_list(table_data = data_of_project , table_column = project_column)
        logger.info("Data formatted successfully. Ready for sending it to Webpage")
    
    except Exception as e:
        logger.error(f"Error executing query or while formatting the Data: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while rendering the filter employee for project page")
    
    else:
        return templates.TemplateResponse("filter_employee_for_project.html",{"request":request, "workers":workers , "projects":projects , "manager":{"manager_id":manager_id}})

@manager_router.post(r"/request_for_employee", response_class=JSONResponse)
async def request_employee(request:Request , employee_data: RequestForEmployee, db = Depends(get_db)) -> None:
    
    """    
    Manager Request for Employee is Processed Here

    Args:
        request (Request): Holds information of incomming HTTP request.
        employee_data (RequestForEmployee): Fetch manager and Employee data.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json :{"message":"Request for employee sent Successfully"}

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"Requset Recieved of Manager asking for Employee: {employee_data.emp_id} in Project: {employee_data.project_id}")
    sql, cursor = db
    sql_query_for_employee_request = f"""
    INSERT INTO manager_request_for_employees (emp_id, manager_id, project_id,admin_id,status)
    WITH request_details AS(
    SELECT '{employee_data.emp_id}' , '{employee_data.manager_id}' , '{employee_data.project_id}' , admin_id , 'Pending'
    FROM manager 
    WHERE manager_id = '{employee_data.manager_id}'
    )
    SELECT * FROM request_details ;"""
    logger.debug(f" SQL Query to save the Manager Request of Employee for his Project")

    try:
        cursor.execute("START TRANSACTION;")
        cursor.execute(sql_query_for_employee_request)
        sql.commit()
        logger.info(f"Manager Request of Employee Saved Successfully")

    except Exception as e:
        logger.error(f"Error executing query : {e}")
        sql.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while sending manager request")
    
    else:
        redirect_url = request.url_for("get_filtered_employees")
        return JSONResponse(content = {"message":"Request for employee sent Successfully"})



@manager_router.get(r"/projects_manager_have")
async def project_manager_have(request: Request, manager_id: str = Depends(get_user), db = Depends(get_db)) -> None:
    
    """    
    Project Manager Have Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        manager_id (String): Fetch manager_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] :manager_project_info.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"{manager_id} : Accessed Project Manager Have Page")

    sql, cursor = db
    sql_query_to_fetch_project = f"""SELECT p.project_id , p.project_name , p.start_date , p.dead_line, p.status , p.description
    FROM  project AS p
    INNER JOIN manager_project_details AS mpd
    ON mpd.project_id = p.project_id
    WHERE mpd.manager_id = '{manager_id}';
    """

    logger.debug(f"SQL Query to See the Project that Manager Have ")

    table_column_project_information = ["project_id", "project_name","start_date","dead_line","status","description"]
    
    try:
        cursor.execute(sql_query_to_fetch_project)
        table_data_for_project = cursor.fetchall()
        logger.info(f"All Project Fetched that Manager Have")

        data_formatter = DataFormatter()
        projects = data_formatter.dictionary_list(table_data = table_data_for_project, table_column=table_column_project_information)
        logger.info("Data formatted successfully. Ready for sending it to Webpage")
    
    except Exception as e:
        logger.error(f"Error executing query or while formatting the Data: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while rendering the mangers project page")
    
    else:
        return templates.TemplateResponse("manager_project_info.html",{"request":request, "projects":projects})

@manager_router.get("/update_project_status")
async def update_project_status_page(request: Request, manager_id = Depends(get_user), db = Depends(get_db)):
    
    """    
    Update Project Status Page

    Args:
        request (Request): Holds information of incomming HTTP request.
        manager_id (String): Fetch manager_id from UserSession.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] :update_project_status.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info(f"{manager_id} : Accessed update Project Status Page")
    sql, cursor = db
    sql_query_to_fetch_project = f"""SELECT p.project_id , p.project_name , p.start_date , p.dead_line, p.status , p.description
    FROM  project AS p
    INNER JOIN manager_project_details AS mpd
    ON mpd.project_id = p.project_id
    WHERE mpd.manager_id = '{manager_id}';
    """
    logger.debug(f"SQL Query to See the Project that Manager Have ")

    table_column_project_information = ["project_id", "project_name","start_date","dead_line","status","description"]
    
    try:
        cursor.execute(sql_query_to_fetch_project)
        table_data_for_project = cursor.fetchall()
        logger.info(f"All Project Fetched that Manager Have")

        data_formatter = DataFormatter()
        projects = data_formatter.dictionary_list(table_data = table_data_for_project, table_column=table_column_project_information)
        logger.info("Data formatted successfully. Ready for sending it to Webpage")
    
    except Exception as e:
        logger.error(f"Error executing query or while formatting the Data: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while rendering the update project status page")
    
    else:
        status_list = [ "Started" , "In Progress" ,"Review" , "Completed"]
        return templates.TemplateResponse("update_project_status.html",{"request":request, "projects":projects, "status_list":status_list , "manager":{"manager_id": manager_id}})


@manager_router.put("/update_project_status")
async def update_project_status(request: Request, project_info: Project_Update_Status, db = Depends(get_db)):
    
    """    
    Update Project Status Request is Processed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        project_info (Project_Update_status): Fetch project status Manager want to Update.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json :{"message": "Project status Updated Successfully"}

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logger.info("Recieved Request to update the status of the Project")
    sql , cursor = db
    sql_query_to_update_project_status = f"""
    UPDATE project 
    SET status = '{project_info.status}'
    WHERE project_id = '{project_info.project_id}';
    """

    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_update_project_status)
        sql.commit()
    
    except Exception as e:
        sql.rollback()
        logger.error(f"error in updating status of the project : {e}")
        raise HTTPException(status_code=500, detail="An error occurred while while updating status of the project")
    
    else:
        return JSONResponse(status_code= status.HTTP_200_OK , content= {"message": "Project status Updated Successfully"})


@manager_router.post("/manager_logout",response_class = HTMLResponse)
async def logout(request: Request):
    manager_user.logout()
    logger.info(f"Manager Logout Successfully")
    return JSONResponse(content= {"message": "Manager Successfully Logout"})


