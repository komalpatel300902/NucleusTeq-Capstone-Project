"""
1: Accept / Reject joining request
2: View all manager , employee and projects
3: Admin can assign and unassign project to employees
4: Admin can approve/ reject manager request for resource
5: Delete employee (include manager)
6: Update employee detail
"""
from fastapi import APIRouter, Request , Form , status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse , RedirectResponse
from config.db_connection import sql,cursor
from schema.schemas import DataFormatter
from models.index_model import JoiningRequest
from models.employee_model import AcceptJoiningRequest , RejectJoiningRequest, RemoveEmployee,RemoveManager, UpdateSkill
from models.project_model import (ProjectDetails, 
                                  ManagerRequestForEmployees, 
                                  AssignProjectToEmployee,
                                  AssignProjectToManager, 
                                  UnassignPtojectToEmployee,
                                  UnassignPtojectToManager)
import json
from datetime import datetime

admin_router = APIRouter()
admin_id ="ADM001" # i have to se this



templates = Jinja2Templates(directory="templates/admin")

@admin_router.get(r"/admin_login", response_class = HTMLResponse)
async def admin_login(request : Request) -> None:
    return templates.TemplateResponse("index.html",{"request":request})

@admin_router.post(r"/admin_login", response_class = HTMLResponse)
async def login(request : Request, username: str = Form(...) , password: str = Form(...) ) -> None:
    sql_query_to_check_admin = f"""SELECT COUNT(admin_id) ,admin_id, password 
    FROM admin
    WHERE admin_id = '{username}' ;
    """
    print(username , password )
    try:
        cursor.execute(sql_query_to_check_admin)
        data = cursor.fetchall()
        condition = data[0][0]
        passwd = data[0][2]
        if condition:
            if passwd == password:
                global admin_id 
                admin_id = username
                redirect_url = request.url_for('get_joining_request')
                print(redirect_url)
                return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
      
            else:
                return json.dumps({"message":"Invalid Password"})
        else:
            return json.dumps({"message":"No such User Exists."})
    except Exception as e:
        print(e)

@admin_router.get("/admin_home", response_class = HTMLResponse)
def admin_home(request: Request):
    return templates.TemplateResponse("home.html",{"request":request})

@admin_router.get(r"/joining_request", response_class = HTMLResponse)
async def get_joining_request(request : Request) -> None:
    try:
        sql_query_for_schema = """DESCRIBE joining_request;"""
        cursor.execute(sql_query_for_schema)
        schema = cursor.fetchall()
        
        sql_query_for_data = f"""SELECT jr.id , jr.name, jr.emp_type, jr.admin_id, jr.email, jr.mobile, jr.gender, jr.date_of_joining, a.admin_name
        FROM joining_request AS jr , admin AS a
        WHERE jr.status = 'Pending' AND jr.admin_id = '{admin_id}' AND a.admin_id = '{admin_id}';"""
        cursor.execute(sql_query_for_data)
        table_data = cursor.fetchall()
        table_columns = ["id","name","emp_type","admin_id","email","mobile","gender","date_of_joining","admin_name"]

        data_formatter = DataFormatter()
        formatted_data = data_formatter.dictionary_list(table_data = table_data,table_column=table_columns)
    except Exception as e:
        print(e)
    else:
        print(formatted_data)
        return templates.TemplateResponse("joining_request.html",context={"request": request ,"data": formatted_data})


@admin_router.post(r"/accept_joining_request", response_class = HTMLResponse)
async def accept_joining_request(request : Request, joining_request: AcceptJoiningRequest ):
    if joining_request.emp_type == "Employee":
        query_to_insert_date_in_table = f"""INSERT INTO employees (emp_id,emp_name,password,admin_id,email,mobile,gender,skills)
        SELECT id, name, password, admin_id, email,mobile , gender, 'None'
        FROM joining_request
        WHERE id = '{joining_request.id}';
        """
    elif joining_request.emp_type == "Manager":
        query_to_insert_date_in_table = f"""INSERT INTO manager (manager_id,manager_name,password,admin_id,email,mobile,gender)
        SELECT id, name, password, admin_id, email, mobile, gender
        FROM joining_request 
        WHERE id = '{joining_request.id}';
        """
    query_to_update_status_of_joining_request = f"""
    UPDATE joining_request
    SET status = 'Approved'
    WHERE id = '{joining_request.id}';
    """
    try:
        cursor.execute(query_to_insert_date_in_table)
        cursor.execute(query_to_update_status_of_joining_request)
        sql.commit()
    except Exception as e:
        print(e)
    else:
        redirect_url = request.url_for("get_joining_request")
        return RedirectResponse(redirect_url ,status.HTTP_303_SEE_OTHER)

@admin_router.post(r"/reject_joining_request", response_class = HTMLResponse)
async def reject_joining_request(request : Request, joining_request: RejectJoiningRequest) -> None:
    query_to_update_status_of_joining_request = f"""
    UPDATE joining_request
    SET status = 'Rejected'
    WHERE id = '{joining_request.id}';
    """
    try:
        cursor.execute(query_to_update_status_of_joining_request)
        sql.commit()
    except Exception as e:
        print(e)
    else:
        redirect_url = request.url_for("get_joining_request")
        return RedirectResponse(redirect_url ,status.HTTP_303_SEE_OTHER)




@admin_router.get(r"/create_project_form", response_class = HTMLResponse)
async def create_project_form(request: Request):
    sql_query_to_get_manager_detail = f"""SELECT manager_id, manager_name
    FROM manager
    WHERE admin_id = '{admin_id}';"""
    table_columns = ["admin_id"]
    try:
        cursor.execute(sql_query_to_get_manager_detail)
        manager_table_column = ["manager_id","manager_name"]
        manager_data = cursor.fetchall()
        data_formatter = DataFormatter()
        managers = data_formatter.dictionary_list(table_data=manager_data, table_column=manager_table_column)

    except Exception as e:
        print(e)
    else:
        return templates.TemplateResponse("create_project.html",{"request":request, "managers":managers})



@admin_router.post(r"/create_project_form_processing",response_class=HTMLResponse)
async def create_project_form_processing(request: Request, project_details: ProjectDetails ):
    # status values ["Not Assigned", "Started" , "In Progress" ,"Review" , "On Hold"]
    if project_details.assign_to == "Later":
        project_assigned = "NO"
        status_value = "Not Assigned"
    else:
        project_assigned = "YES"
        status_value = "Started"
        sql_query_to_insert_manager_project_details = F"""
        INSERT INTO manager_project_details (manager_id , project_id)
        VALUES ('{project_details.assign_to}','{project_details.project_id}');
        """

    start_date = datetime.now().strftime('%Y-%m-%d')
    
    sql_query_to_create_project = f"""INSERT INTO project (project_id ,project_name, admin_id, start_date, dead_line, status, project_assigned, project_completion_date, description)
    VALUES(
        '{project_details.project_id}',
        '{project_details.project_name}', 
        '{admin_id}',
        '{start_date}',
        '{project_details.dead_line}',
        '{status_value}',
        '{project_assigned}',
        NULL,
        '{project_details.description}'
    );
    """
    print(sql_query_to_create_project)

    try:
        cursor.execute(sql_query_to_create_project)
        cursor.execute(sql_query_to_insert_manager_project_details)
        sql.commit()
    except Exception as e:
        print(e)
    else:
        redirect_url = request.url_for("fetch_all_employees_and_project_for_admin")
        return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

@admin_router.get(r"/admin_view_all",response_class=HTMLResponse)
async def fetch_all_employees_and_project_for_admin(request : Request)->None:

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

    table_column_all_information = ["emp_id", "emp_name","gender","email","admin_id","admin_name","manager_id","manager_name","project_id","project_name"]
    table_column_manager_information = ["manager_id", "manager_name","gender","email","admin_id","admin_name","project_id","project_name"]
    table_column_project_information = ["project_id", "project_name","admin_id","admin_name","start_date","dead_line","manager_id","manager_name","status"]
    
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


@admin_router.get(r"/assign_project",response_class=HTMLResponse)
async def get_employee_for_assigning_project(request : Request)->None: 
    sql_query_to_get_employee_detail = f"""
    SELECT e.emp_id, e.emp_name, e.gender, e.mobile, e.email, e.skills
    FROM employees AS e
    WHERE project_assigned IN ('NO','') AND admin_id = '{admin_id}'; """ 

    sql_query_for_project_given_to_employee = f"""SELECT p.project_id, p.project_name 
    FROM project AS p
    INNER JOIN manager_project_details AS mpd
    ON mpd.project_id = p.project_id
    WHERE p.project_assigned = "YES";""" 

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

    sql_query_for_project_given_to_manager = f"""SELECT project_id, project_name 
    FROM project 
    WHERE project_assigned = 'NO' ;""" 

    try:
        cursor.execute(sql_query_to_get_employee_detail)
        employee_data = cursor.fetchall()
        cursor.execute(sql_query_to_get_manager_details)
        manager_data = cursor.fetchall()
        cursor.execute(sql_query_for_project_given_to_employee)
        employee_project_options = cursor.fetchall()
        cursor.execute(sql_query_for_project_given_to_manager)
        manager_project_options = cursor.fetchall()

        employee_table_column = ["emp_id","emp_name","gender","mobile","email","skills"]
        employee_project_column = ["project_id","project_name"]

        manager_table_colum = ["manager_id","manager_name","gender","mobile","email","project_id","project_name"] 
        manager_project_column = ["project_id","project_name"]

        data_formatter = DataFormatter()
        employees = data_formatter.dictionary_list(table_data=employee_data , table_column=employee_table_column)
        employee_projects = data_formatter.dictionary_list(table_data = employee_project_options , table_column = employee_project_column)

        managers = data_formatter.dictionary_list(table_data = manager_data , table_column = manager_table_colum)
        manager_projects = data_formatter.dictionary_list(table_data = manager_project_options , table_column = manager_project_column)
    except Exception as e:
        print(e)
    else: 
        return templates.TemplateResponse("assign_project.html",{"request": request, "employees":employees,"managers":managers,"manager_projects": manager_projects , "employee_projects":employee_projects })


@admin_router.post(r"/assign_employee_a_project",response_class=HTMLResponse)
async def assign_project_to_employees(request : Request ,employee_data : AssignProjectToEmployee )->None:
    
    sql_query_to_insert_record = f"""
    INSERT INTO employee_project_details (emp_id,manager_id,project_id)
    WITH employee_project_data AS (
    SELECT '{employee_data.emp_id}' AS emp_id, mpd.manager_id AS manager_id ,'{employee_data.project_id}' AS project_id 
    FROM manager_project_details AS mpd
    WHERE mpd.project_id = '{employee_data.project_id}'
    )
    SELECT emp_id , manager_id , project_id FROM employee_project_data ;"""    
    print(sql_query_to_insert_record)
    sql_query_to_update = f"""UPDATE employees
    SET project_assigned = "YES"
    WHERE emp_id = '{employee_data.emp_id}' ;"""

    try:
        cursor.execute(sql_query_to_insert_record)
        cursor.execute(sql_query_to_update)
        sql.commit()
    except Exception as e:
        print(e)
    else: 
        redirect_url = request.url_for("get_employee_for_assigning_project")
        return RedirectResponse(redirect_url, status.HTTP_303_SEE_OTHER)

@admin_router.post(r"/assign_manager_a_project",response_class=HTMLResponse)
async def assign_project_to_employees(request : Request , manager_data: AssignProjectToManager ):
    sql_query_to_insert_data = f"""INSERT INTO manager_project_details (manager_id,project_id)
    VALUES('{manager_data.manager_id}','{manager_data.project_id}');"""

    sql_query_to_update_project_table = f"""UPDATE project
    SET project_assigned = 'YES'
    WHERE project_id = '{manager_data.project_id}' ;"""
    try:
        cursor.execute(sql_query_to_insert_data)
        cursor.execute(sql_query_to_update_project_table)
        sql.commit()

    except Exception as e:
        print(e)
    else: 
        redirect_url = request.url_for("get_employee_for_assigning_project")
        return RedirectResponse(redirect_url, status.HTTP_303_SEE_OTHER)



@admin_router.get(r"/unassign_project",response_class=HTMLResponse)
async def unassign_project_page(request : Request)->None:
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

    employee_table_column = ["emp_id","emp_name","gender","mobile","email","project_id", "project_name","manager_id","manager_name"]
    manager_table_column = ["manager_id", "manager_name","gender","mobile","email","project_id","project_name"]
    try:
        cursor.execute(sql_query_to_find_employee_project)
        employee_data = cursor.fetchall()
        cursor.execute(sql_query_to_find_manager_project)
        manager_data = cursor.fetchall()
        data_formatter = DataFormatter()
        employees = data_formatter.dictionary_list(table_data = employee_data, table_column=employee_table_column)
        managers = data_formatter.dictionary_list(table_data = manager_data, table_column=manager_table_column)
    except Exception as e:
        print(e)
    else:
        return templates.TemplateResponse("unassign_project.html",{"request":request,"employees":employees,"managers":managers})

@admin_router.put(r"/unassign_employee_from_project",response_class=HTMLResponse)
async def unassig_employee_from_project(request : Request, employee_data : UnassignPtojectToEmployee  )->None:
    sql_query_to_unassign_employee_from_project = f"""
    DELETE FROM employee_project_details
    WHERE emp_id = '{employee_data.emp_id}' ;
    """

    sql_query_to_update_employee_table = f"""UPDATE employees
    SET project_assigned = 'NO'
    WHERE emp_id = '{employee_data.emp_id}' AND admin_id = '{admin_id}' ;"""
    
    try:
        cursor.execute(sql_query_to_unassign_employee_from_project)
        cursor.execute(sql_query_to_update_employee_table)
        sql.commit()
    except Exception as e:
        print(e)
    else:
        redirect_url = request.url_for("unassign_project_page")
        return RedirectResponse(redirect_url,status.HTTP_303_SEE_OTHER)

@admin_router.put(r"/unassign_manager_from_project",response_class=HTMLResponse)
async def unassig_manager_from_project(request : Request, manager_data: UnassignPtojectToManager )->None:
    sql_query_to_update_manager_project_details =  f"""
    UPDATE manager_project_details
    SET manager_id = 'Unassigned'
    WHERE manager_id = '{manager_data.manager_id}' AND project_id = '{manager_data.project_id}' ;
    """
    sql_query_to_update_project = f"""UPDATE project
    SET project_assigned = 'NO',
    status = 'On Hold'
    WHERE project_id = '{manager_data.project_id}'; """

    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_update_manager_project_details)
        cursor.execute(sql_query_to_update_project)
        
    except Exception as e:
        sql.rollback()
        print(e)
    else:
        sql.commit()
        redirect_url = request.url_for("unassign_project_page")
        return RedirectResponse(redirect_url,status.HTTP_303_SEE_OTHER)

@admin_router.get(r"/manager_request",response_class=HTMLResponse)
async def get_manager_request(request : Request)-> None:
    sql_query_for_manager_request = f"""
    SELECT m.manager_name, m.manager_id, p.project_name , p.project_id , e.emp_name , e.emp_id
    FROM manager_request_for_employees AS mrfe
    INNER JOIN manager AS m
    ON mrfe.manager_id = m.manager_id
    INNER JOIN project AS p
    ON mrfe.project_id = p.project_id
    INNER JOIN employees AS e
    ON mrfe.emp_id = e.emp_id
    WHERE mrfe.status = "Pending" AND mrfe.admin_id = '{admin_id}';
    """
    try:
        cursor.execute(sql_query_for_manager_request)
        table_column = ["manager_name", "manager_id","project_name","project_id","emp_name","emp_id"]
        data = cursor.fetchall()
        data_formatter = DataFormatter()
        data_entries = data_formatter.dictionary_list(table_data=data, table_column=table_column)
    except Exception as e:
        print(e)
    else: 
        return templates.TemplateResponse("manager_request.html",{"request":request,"data_entries":data_entries})

@admin_router.post(r"/accept_manager_request",response_class=HTMLResponse)
async def accept_manager_request(request : Request, manager_request_for_employees: ManagerRequestForEmployees):
    sql_to_insert_record = f"""
    INSERT INTO employee_project_details (emp_id,project_id,manager_id)
    VALUES ('{manager_request_for_employees.emp_id}', '{manager_request_for_employees.project_id}', '{manager_request_for_employees.manager_id}')"""

    sql_query_to_update = f"""
    UPDATE manager_request_for_employees
    SET status = 'Approved'
    WHERE emp_id = '{manager_request_for_employees.emp_id}' AND project_id = '{manager_request_for_employees.project_id}' AND manager_id = '{manager_request_for_employees.manager_id}';
    """

    sql_query_to_update_employee_record = f"""
    UPDATE employees
    SET project_assigned = 'YES'
    WHERE emp_id = '{manager_request_for_employees.emp_id}';"""

    try:
        cursor.execute(sql_to_insert_record)
        cursor.execute(sql_query_to_update_employee_record)
        cursor.execute(sql_query_to_update)
        sql.commit()
    except Exception as e:
        print(e)
    else: 
        redirect_url = request.url_for('get_manager_request')
        return RedirectResponse(redirect_url,status.HTTP_303_SEE_OTHER)
    
@admin_router.put(r"/reject_manager_request",response_class=HTMLResponse)
async def reject_manager_request(request : Request, manager_request_for_employees: ManagerRequestForEmployees):
    
    sql_query_to_update = f"""
    UPDATE manager_request_for_employees
    SET status = 'Rejected'
    WHERE emp_id = '{manager_request_for_employees.emp_id}' AND project_id = '{manager_request_for_employees.project_id}' AND manager_id = '{manager_request_for_employees.manager_id}';
    """
    try:
        cursor.execute(sql_query_to_update)
        sql.commit()
    except Exception as e:
        print(e)
    else: 
        redirect_url = request.url_for('get_manager_request')
        return RedirectResponse(redirect_url,status.HTTP_303_SEE_OTHER)
    
@admin_router.get(r"/remove_workers",response_class=HTMLResponse)
async def remove_employees_page(request : Request)-> None:
    query_for_manager = f"""
    SELECT manager_name, manager_id, email,mobile , gender
    FROM manager
    WHERE admin_id = '{admin_id}'"""
    query_for_employee = f"""
    SELECT emp_name, emp_id, email,mobile , gender
    FROM employees
    WHERE admin_id = '{admin_id}'"""

    table_column = ["name","id","email","mobile","gender"]
    try:
        cursor.execute(query_for_manager)
        manager_data = cursor.fetchall()
        cursor.execute(query_for_employee)
        employee_data = cursor.fetchall()
        data_formatter = DataFormatter()
        manager_data_entries = data_formatter.dictionary_list(table_data=manager_data, table_column=table_column)
        employees_data_entries = data_formatter.dictionary_list(table_data=employee_data, table_column=table_column)
    except Exception as e:
        print(e)
    else:
        return templates.TemplateResponse("remove_employee.html",{"request":request,"managers":manager_data_entries,"employees":employees_data_entries})


#[In Progress]
@admin_router.delete("/remove_manager",response_class=HTMLResponse)
async def remove_manager(request : Request , manager_data : RemoveManager)-> None:
    sql_query_to_store_record = f"""
    INSERT INTO employee_termination_records (id,name,emp_type,admin_id,admin_name,email,mobile,gender,date_of_joining,departure_date)
    WITH manager_data AS(
        SELECT m.manager_id , m.manager_name ,'Manager', m.admin_id , a.admin_name , m.email , m.mobile , m.gender , jr.date_of_joining, CURDATE()
        FROM manager AS m
        INNER JOIN admin AS a
        ON a.admin_id = m.admin_id
        INNER JOIN joining_request AS jr
        ON m.manager_id = jr.id AND m.admin_id = jr.admin_id
        WHERE m.admin_id = '{admin_id}' AND m.manager_id = '{manager_data.manager_id}'
    )
    SELECT * FROM manager_data;
    """

    sql_query_to_remove_manager = f"""
    DELETE FROM manager
    WHERE manager_id = '{manager_data.manager_id}' AND  admin_id = '{admin_id}';
    """

    sql_query_for_updating = f"""UPDATE manager_project_details
    set manager_id = 'Terminated'
    WHERE manager_id = '{manager_data.manager_id}';
    """

    sql_query_to_update_project = f"""UPDATE project
    SET project_assigned = 'NO'
    WHERE project_id in (
        SELECT project_id FROM manager_project_details WHERE manager_id = '{manager_data.manager_id}'
        );
    """ 
    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_store_record)
        cursor.execute(sql_query_to_remove_manager)
        cursor.execute(sql_query_for_updating)
        cursor.execute(sql_query_to_update_project)
    except Exception as e:
        sql.rollback()
        print(e)
    else:
        sql.commit()
        redirect_url = request.url_for('remove_employees_page')
        return RedirectResponse(redirect_url,status.HTTP_303_SEE_OTHER)
    

@admin_router.delete("/remove_employee",response_class=HTMLResponse)
async def remove_employee(request : Request , employee_data: RemoveEmployee)-> None:
    sql_query_to_remove_employee = f"""
    DELETE FROM employees
    WHERE emp_id = '{employee_data.emp_id}' AND  admin_id = '{admin_id}';
    """
    print(sql_query_to_remove_employee)
    try:
        cursor.execute("START TRANSACTION;")
        cursor.execute(sql_query_to_remove_employee)
    except Exception as e:
        sql.rollback()
        print(e)
    else:
        sql.commit()
        redirect_url = request.url_for('remove_employees_page')
        return RedirectResponse(redirect_url,status.HTTP_303_SEE_OTHER)
    

#[In Progress]
@admin_router.get(r"/update_employee_skill",response_class=HTMLResponse)
async def update_employees_skill(request : Request) -> None:
    sql_query_to_get_employee_details = f"""SELECT e.emp_id, e.emp_name, e.gender, e.mobile, e.email, e.skills
    FROM employees AS e
    WHERE admin_id = '{admin_id}'; """
    try:
        cursor.execute(sql_query_to_get_employee_details)
        employee_data = cursor.fetchall()
        employee_table_column = ["emp_id","emp_name","gender","mobile","email","skills"]
        data_formatter = DataFormatter()
        employees = data_formatter.dictionary_list(table_data=employee_data,table_column=employee_table_column)

    except Exception as e:
        print(e)
    else:
        return templates.TemplateResponse("update_skill.html",{"request": request,"employees":employees}) 

@admin_router.put(r"/add_employee_skill",response_class=HTMLResponse)
async def update_employees_skill(request : Request, employee_data: UpdateSkill) -> None:
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
        redirect_url = request.url_for("update_employees_skill")
        return RedirectResponse(redirect_url, status.HTTP_303_SEE_OTHER)

@admin_router.put(r"/replace_employee_skill",response_class=HTMLResponse)
async def update_employees_skill(request : Request, employee_data: UpdateSkill) -> None:
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
        redirect_url = request.url_for("update_employees_skill")
        return RedirectResponse(redirect_url, status.HTTP_303_SEE_OTHER)
    
@admin_router.get("/logout",response_class = HTMLResponse)
async def logout():
    ...
