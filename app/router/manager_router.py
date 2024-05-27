"""
1: able to view all the employees, manager and projects.
2: filter employees by skill and uassigned employees.
3: request employees to admin
4: see all theproject on which manager is working
""" 

from fastapi import APIRouter, HTTPException , Request , status, Depends , Response 
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse , RedirectResponse, JSONResponse
from models.employee_model import RequestForEmployee
from models.index_model import LoginDetails
from config.db_connection import get_db
from schema.schemas import DataFormatter


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
    return manager_user.manager_id

manager_router = APIRouter()


templates = Jinja2Templates(directory = "templates/manager")
@manager_router.get("/manager_login")
async def manager_login(request: Request):
    return templates.TemplateResponse("index.html",{"request":request}) 

@manager_router.post(r"/manager_login_data", response_class = HTMLResponse)
async def manager_credential_authentication(response: Response,request : Request, login_details: LoginDetails, db = Depends(get_db)) -> None:

    sql , cursor = db

    sql_query_to_check_admin = f"""SELECT COUNT(manager_id) ,manager_id, password 
    FROM manager
    WHERE manager_id = '{login_details.username}' AND password = '{login_details.password}' ;
    """
    print( "manager",login_details.username , login_details.password )
    try:
        cursor.execute(sql_query_to_check_admin)
        data = cursor.fetchall()
    except Exception as e:
        print(e)
    else:
        condition = data[0][0]
        print(type(condition))
        if condition:
            manager_user.login(login_details.username)
            redirect_url = request.url_for('admin_home')
            print(redirect_url)
            return JSONResponse(content={"message":"Login Successful"})
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")

      

@manager_router.get("/manager_home")
async def manager_home(request: Request):
    return templates.TemplateResponse("home.html",{"request":request}) 


@manager_router.get(r"/comprehensive_info")
async def get_all_employees_and_project(request: Request, db = Depends(get_db)) -> None:

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

    sql_query_to_get_manager_information = f"""SELECT m.manager_id, m.manager_name, m.gender, m.email,m.admin_id,a.admin_name , GROUP_CONCAT(mpd.project_id) , GROUP_CONCAT(p.project_name)
    FROM manager AS m
    LEFT JOIN manager_project_details AS mpd
    ON m.manager_id = mpd.manager_id
    LEFT JOIN project AS p
    ON p.project_id = mpd.project_id
    LEFT JOIN admin AS a
    ON a.admin_id = m.admin_id
    GROUP BY m.manager_id ;"""

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

    table_column_all_information = ["emp_id", "emp_name","gender","email","admin_id","admin_name","manager_id","manager_name","project_id","project_name"]
    table_column_manager_information = ["manager_id", "manager_name","gender","email","admin_id","admin_name","project_id","project_name"]
    table_column_project_information = ["project_id", "project_name","admin_id","admin_name","start_date","dead_line","manager_id","manager_name"]
    
    try:
        cursor.execute(sql_query_to_get_all_information)
        table_data_for_worker = cursor.fetchall()
        cursor.execute(sql_query_to_get_manager_information)
        table_data_for_manager = cursor.fetchall()
        cursor.execute(sql_query_to_get_project_information)
        table_data_for_project = cursor.fetchall()
        data_formatter = DataFormatter()
        workers = data_formatter.dictionary_list(table_data = table_data_for_worker, table_column=table_column_all_information)
        managers = data_formatter.dictionary_list(table_data = table_data_for_manager, table_column=table_column_manager_information)
        projects = data_formatter.dictionary_list(table_data = table_data_for_project, table_column=table_column_project_information)
    except Exception as e:
        print(e)
    else:
        return templates.TemplateResponse("comprehensive_info.html",{"request":request, "managers": managers,"workers":workers, "projects":projects})


@manager_router.get(r"/filtered_employee")
async def get_filtered_employees(request: Request, manager_id: str = Depends(get_user), db = Depends(get_db) ) -> None:
    sql , cursor = db
    sql_query_to_fetch_employees = f"""SELECT e.emp_id , e.emp_name , e.gender , e.mobile , e.email , e.skills
    FROM employees AS e,manager AS m
    WHERE m.manager_id = '{manager_id}' AND e.admin_id = m.admin_id and e.project_assigned = 'NO';
    """
    sql_query_to_fetch_projects = f"""SELECT mpd.project_id , p.project_name
    FROM manager_project_details AS mpd
    INNER JOIN project AS p
    ON p.project_id = mpd.project_id
    WHERE mpd.manager_id = '{manager_id}';
    """


    table_column_employee_information = ["emp_id", "emp_name","gender","mobile","email","skills"]
    project_column = ["project_id","project_name"]
    try:
        cursor.execute(sql_query_to_fetch_employees)
        table_data_for_employee_request = cursor.fetchall()
        cursor.execute(sql_query_to_fetch_projects)
        data_of_project = cursor.fetchall()
        data_formatter = DataFormatter()
        workers = data_formatter.dictionary_list(table_data = table_data_for_employee_request, table_column=table_column_employee_information)
        projects = data_formatter.dictionary_list(table_data = data_of_project , table_column = project_column)
    except Exception as e:
        print(e)
    else:
        return templates.TemplateResponse("filter_employee_for_project.html",{"request":request, "workers":workers , "projects":projects , "manager":{"manager_id":manager_id}})

@manager_router.post(r"/request_for_employee", response_class=JSONResponse)
async def request_employee(request:Request , employee_data: RequestForEmployee, db = Depends(get_db)) -> None:
    sql, cursor = db
    sql_query_for_employee_request = f"""
    INSERT INTO manager_request_for_employees (emp_id, manager_id, project_id,admin_id,status)
    WITH request_details AS(
    SELECT '{employee_data.emp_id}' , '{employee_data.manager_id}' , '{employee_data.project_id}' , admin_id , 'Pending'
    FROM manager 
    WHERE manager_id = '{employee_data.manager_id}'
    )
    SELECT * FROM request_details ;"""

    try:
        cursor.execute("START TRANSACTION;")
        cursor.execute(sql_query_for_employee_request)
    except Exception as e:
        sql.rollback()
        print(e)
    else:
        sql.commit()
        redirect_url = request.url_for("get_filtered_employees")
        return JSONResponse(content = {"message":"Request for employee sent Successfully"})



@manager_router.get(r"/projects_manager_have")
async def project_manager_have(request: Request, manager_id: str = Depends(get_user), db = Depends(get_db)) -> None:
    sql, cursor = db
    sql_query_to_fetch_project = f"""SELECT p.project_id , p.project_name , p.start_date , p.dead_line, p.status , p.description
    FROM  project AS p
    INNER JOIN manager_project_details AS mpd
    ON mpd.project_id = p.project_id
    WHERE mpd.manager_id = '{manager_id}';
    """
    table_column_project_information = ["project_id", "project_name","start_date","dead_line","status","description"]
    
    try:
        cursor.execute(sql_query_to_fetch_project)
        table_data_for_project = cursor.fetchall()
        data_formatter = DataFormatter()
        projects = data_formatter.dictionary_list(table_data = table_data_for_project, table_column=table_column_project_information)
    except Exception as e:
        print(e)
    else:
        return templates.TemplateResponse("manager_project_info.html",{"request":request, "projects":projects})

@manager_router.post("/manager_logout",response_class = HTMLResponse)
async def logout(request: Request):
    manager_user.logout()
    return JSONResponse(content= {"message": "Manager Successfully Logout"})


