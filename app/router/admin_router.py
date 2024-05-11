"""
1: Accept / Reject joining request
2: View all manager , employee and projects
3: Admin can assign and unassign project to employees
4: Admin can approve/ reject manager request for resource
5: Delete employee (include manager)
6: Update employee detail
"""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from config.db_connection import sql,cursor
from schema.schemas import DataFormatter
from models.index_model import JoiningRequest
from models.project_model import ProjectDetails, ManagerRequestForEmployees

admin_router = APIRouter()
admin_id ="ADM001" # i have to se this


templates = Jinja2Templates(directory="templates/admin")
@admin_router.get(r"/login", response_class = HTMLResponse)
async def login(request : Request) -> None: ...

@admin_router.get(r"/joining_request", response_class = HTMLResponse)
async def get_joining_request(request : Request) -> None:
    try:
        sql_query_for_schema = """DESCRIBE joining_request;"""
        cursor.execute(sql_query_for_schema)
        schema = cursor.fetchall()
        
        sql_query_for_data = f"""SELECT * 
        FROM joining_request
        WHERE status <> 'Approve' AND admin_id = '{admin_id}';"""
        cursor.execute(sql_query_for_data)
        table_data = cursor.fetchall()

        data_formatter = DataFormatter()
        formatted_data = data_formatter.dictionary_list(table_data = table_data,schema = schema)
    except Exception as e:
        print(e)
    else:
        print(formatted_data)
        return templates.TemplateResponse("joining_request.html",context={"request": request ,"data": formatted_data})


@admin_router.post(r"/accept_joining_request", response_class = HTMLResponse)
async def joining_request(request : Request, joining_request: JoiningRequest ):
    if joining_request.emp_type == "Employee":
        query_to_insert_date_in_table = f"""INSERT INTO employees ('emp_id','emp_name','password','admin_id','admin_name','email','mobile','gender','skills')
        VALUES ('{joining_request.id}',
                '{joining_request.name}',
                '{joining_request.password}',
                '{joining_request.admin_id}',
                '{joining_request.admin_name}',
                '{joining_request.email}',
                '{joining_request.mobile}',
                '{joining_request.gender}',
                'None'
                );
        """
    elif joining_request.emp_type == "Manager":
        query_to_insert_date_in_table = f"""INSERT INTO manager ('manager_id','manager_name','password','admin_id','admin_name','email','mobile','gender')
        VALUES ('{joining_request.id}',
                '{joining_request.name}',
                '{joining_request.password}',
                '{joining_request.admin_id}',
                '{joining_request.admin_name}',
                '{joining_request.email}',
                '{joining_request.mobile}',
                '{joining_request.gender}'
                );
        """
    query_to_update_status_of_joining_request = f"""
    UPDATE joining_request
    SET status = 'Approved'
    WHERE id = '{joining_request.id}';
    """
    try:
        cursor.execute(query_to_insert_date_in_table)
        cursor.execute(query_to_update_status_of_joining_request)
    except Exception as e:
        print(e)
    else:
        return templates.TemplateResponse("joining_request.html",{"request":request})

@admin_router.post(r"/reject_joining_request", response_class = HTMLResponse)
async def joining_request(request : Request, joining_request: JoiningRequest) -> None:
    query_to_update_status_of_joining_request = f"""
    UPDATE joining_request
    SET status = 'Rejected'
    WHERE id = '{joining_request.id}';
    """
    try:
        cursor.execute(query_to_update_status_of_joining_request)
    except Exception as e:
        print(e)
    else:
        return templates.TemplateResponse("joining_request.html",{"request":request})




@admin_router.get(r"/create_project", response_class = HTMLResponse)
async def create_project(request: Request):
    return templates.TemplateResponse("create_project.html",{"request":request})


@admin_router.post(r"/create_project",response_class=HTMLResponse)
async def create_project(request: Request, project_details: ProjectDetails ):
    query_to_create_project = f"""INSERT INTO project ('project_id','project_name','admin_id','admin_name','start_date','dead_line','status,'project_assigned','project_completion_date')
    VALUES(
        '{project_details.project_id}',
        '{project_details.project_name}', 
        '{project_details.admin_id}',
        '{project_details.admin_name}',
        '{project_details.start_date}',
        '{project_details.dead_line}',
        '{project_details.status}',
        '{project_details.project_assigned}',
        '{project_details.project_completion_date}',
        '{project_details.description}'
    );
    """

@admin_router.get(r"/all",response_class=HTMLResponse)
async def get_all_employees_and_project(request : Request)->None:

    sql_query_for_comprehensive_detail = """
    SELECT a.admin_id, a.admin_name , m.manager_id , m.manager_name , mpd.project_id, epd.emp_id
    FROM admin AS a
    INNER JOIN manager AS m 
    ON a.admin_id = m.admin_id
    INNER JOIN manager_project_details AS mpd
    ON m.manager_id = mpd.manager_id
    INNER JOIN employee_project_details AS epd
    ON epd.manager_id = m.manager_id AND epd.project_id = mpd.project_id
    ;
    """
    table_column = ["admin_id","admin_name","manager_id","manager_name","project_id","emp_id"]
    
    try:
        cursor.execute(sql_query_for_comprehensive_detail)
        data = cursor.fetchall()
        data_formatter = DataFormatter()
        data_entries = data_formatter.dictionary_list(table_data=data, table_column=table_column)
    except Exception as e:
        print(e)
    else:
        return templates.TemplateResponse("comprehensive_info.html",{"request":request,"data_entries": data_entries })


@admin_router.get(r"/assign_project",response_class=HTMLResponse)
async def get_employee_for_assigning_project(request : Request)->None: 
    sql_query_to_get_employee_detail = f"""
    SELECT e.emp_id, e.emp_name, e.gender, e.mobile, e.email, e.skills
    FROM employees AS e
    WHERE project_assigned <> 'Assigned' AND admin_id = '{admin_id}'; """ 

    sql_query_for_project_given_to_employee = f"""SELECT project_id, project_name 
    FROM project 
    WHERE project_assigned = "YES";""" 

    sql_query_to_get_manager_details = f"""
    SELECT m.manager_id , m.manager_name, m.gender, m.mobile, m.email, 
    GROUP_CONCAT(DISTINCT mpd.project_id ORDER BY mpd.project_id ASC SEPARATOR ', ') AS project_they_have,
    GROUP_CONCAT(DISTINCT p.project_name ORDER BY p.project_id ASC SEPARATOR ', ') AS project_names
    FROM manager AS m
    LEFT JOIN manager_project_details AS mpd
    ON m.manager_id = mpd.manager_id
    INNER JOIN project AS p
    ON p.project_id = mpd.project_id
    WHERE m.admin_id = '{admin_id}'
    GROUP BY m.manager_id;
    """

    sql_query_for_project_given_to_manager = f"""SELECT project_id, project_name 
    FROM project 
    WHERE project_assigned = 'NO';""" 

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
async def assign_project_to_employees(request : Request , project_id : str , emp_id:str )->None:
    
    sql_query_to_insert_record = f"""
    WITH employee_project_data AS (
    SELECT '{emp_id}' AS emp_id, m.manager_id AS manager_id ,'{project_id}' AS project_id 
    FROM manager_project_details AS mpd
    WHERE mpd.project_id = '{project_id}';
    )
    INSERT INTO employee_project_details ('emp_id','manager_id','project_id')
    VALUES (SELECT emp_id , manager_id , project_id FROM employee_project_data );"""    
    
    sql_query_to_update = f"""UPDATE employees
    SET project_assigned = "YES"
    WHERE emp_id = '{emp_id}' ;"""

    try:
        cursor.execute(sql_query_to_insert_record)
        cursor.execute(sql_query_to_update)
    except Exception as e:
        print(e)

@admin_router.post(r"/assign_manager_a_project",response_class=HTMLResponse)
async def assign_project_to_employees(request : Request , project_id : str , manager_id:str )->None:
    sql_query_to_insert_data = f"""INSERT INTO manager_project_details ('manager_id','project_id')
    VALUES('{manager_id}','{project_id}');"""
    try:
        cursor.execute(sql_query_to_insert_data)
    except Exception as e:
        print(e)



@admin_router.get(r"/unassign_project",response_class=HTMLResponse)
async def get_unassig_project_employees(request : Request)->None:
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
    p.project_id , p.project_name
    FROM manager_project_details AS mpd
    INNER JOIN manager AS m
    ON m.manager_id = mpd.manager_id
    INNER JOIN project AS p
    ON p.project_id = mpd.project_id
    WHERE m.admin_id = '{admin_id}' ;"""

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
async def unassig_project_employees(request : Request, emp_id: str )->None:
    sql_query_to_unassign_employee_from_project = f"""
    DELETE FROM employee_project_details
    WHERE emp_id = '{emp_id}' ;
    """

    sql_query_to_update_employee_table = f"""UPDATE employees
    SET project_assigned = 'NO'
    WHERE emp_id = '{emp_id}' AND admin_id = '{admin_id}' ;"""
    
    try:
        cursor.execute(sql_query_to_unassign_employee_from_project)
        cursor.execute(sql_query_to_update_employee_table)
    except Exception as e:
        print(e)
    else:
        pass

@admin_router.put(r"/unassign_manager_from_project",response_class=HTMLResponse)
async def unassig_project_employees(request : Request, manager_id: str,project_id :str )->None:
    sql_query_to_update_manager_project_details =  f"""
    UPDATE manager_project_details
    SET manager_id = 'Unassigned'
    WHERE manager_id = '{manager_id}' AND project_id = '{project_id}' ;
    """
    
    try:
        cursor.execute(sql_query_to_update_manager_project_details)
    except Exception as e:
        print(e)
    else:
        pass

@admin_router.get(r"/manager_request",response_class=HTMLResponse)
async def manager_request(request : Request)-> None:
    sql_query_for_manager_request = """
    SELECT m.manager_name, m.manager_id, p.project_name , p.project_id , e.emp_name , e.emp_id
    FROM manager_request_for_employees AS mrfe
    INNER JOIN manager AS m
    ON mrfe.manager_id = m.manager_id
    INNER JOIN project AS p
    ON mrfe.project_id = p.project_id
    INNER JOIN employees AS e
    ON mrfe.emp_id = e.emp_id
    WHERE mrfe.status = "Pending"
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

@admin_router.post(r"/manager_request",response_class=HTMLResponse)
async def manager_request(manager_request_for_employees: ManagerRequestForEmployees,request : Request)-> None:
    sql_to_insert_record = f"""
    INSERT INTO employee_project_details (emp_id,project_id,manager_id)
    VALUES ('{manager_request_for_employees.emp_id}', '{manager_request_for_employees.project_id}', '{manager_request_for_employees.manager_id}')"""

    sql_query_to_update = f"""
    UPDATE manager_request_for_employees
    SET status = 'Approved';
    """

    sql_query_to_update_employee_record = f"""
    UPDATE employees
    SET project_assigned = 'YES';"""
    
@admin_router.get(r"/remove_employees",response_class=HTMLResponse)
async def delete_employees(request : Request)-> None:
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
@admin_router.delete("/remove_manager/{manager_id}",response_class=HTMLResponse)
async def delete_employees(manager_id:str ,request : Request)-> None:
    sql_query_to_store_record = f"""
    WITH manager_data AS(
        SELECT m.manager_id , m.manager_name ,'Manager', m.admin_id , m.admin_name , m.email , m.mobile , m.gender , jr.date_of_joining, CONVERT(date, GETDATE())
        FROM manager AS m
        INNER JOIN joining_request AS jr
        ON m.manager_id = jr.id AND m.admin_id = jr.admin_id
        WHERE m.admin_id = '{admin_id}';
    )
    INSERT INTO employee_termination_records ('id','name','emp_type','admin_id','admin_name','email','mobile','gender','date_of_joining','departure_date')
    VALUES (SELECT * FROM manager_data);
    """

    sql_query_to_remove_manager = f"""
    DELETE FROM manager
    WHERE manager_id = '{manager_id}' AND  admin_id = '{admin_id}';
    """

    sql_query_for_updating = f"""UPDATE manager_project_details
    set manager_id = 'Terminated'
    WHRER manager_id = '{manager_id}'
    """
    try:
        cursor.execute(sql_query_to_store_record)
        cursor.execute(sql_query_to_remove_manager)
        cursor.execute(sql_query_for_updating)
    except Exception as e:
        print(e)
    else:
        # 
        pass

@admin_router.delete("/remove_employee/{emp_id}",response_class=HTMLResponse)
async def delete_employees(emp_id : str, request : Request)-> None:
    sql_query_to_remove_employee = f"""
    DELETE FROM employee
    WHERE emp_id = '{emp_id}' AND  admin_id = '{admin_id}';
    """
    try:
        cursor.execute(sql_query_to_remove_employee)
    except Exception as e:
        print(e)

#[In Progress]
@admin_router.get(r"/update_employee_sill",response_class=HTMLResponse)
async def update_employees_skill(request : Request) -> None:

    return templates.TemplateResponse("update_skill.html",{"request": request}) 

@admin_router.put(r"/add_employee_sill",response_class=HTMLResponse)
async def update_employees_skill(emp_id: str ,skills: str , request : Request) -> None:
    sql_query_to_add_skill = f"""
    UPDATE employees
    SET skills = CONCAT(skills,' {skills}')
    WHERE emp_id = '{emp_id}';
    """
    try:
        cursor.execute(sql_query_to_add_skill)
    except Exception as e:
        print(e)

@admin_router.put(r"/replace_employee_sill",response_class=HTMLResponse)
async def update_employees_skill(emp_id: str, skills: str , request : Request) -> None:
    sql_query_to_replace_skill = f"""
    UPDATE employees
    SET skills = CONCAT(skills,' {skills}')
    WHERE emp_id = '{emp_id}';
    """
    try:
        cursor.execute(sql_query_to_replace_skill)
    except Exception as e:
        print(e)