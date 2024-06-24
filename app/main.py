"""
[main.py] : Starting of app
"""
from fastapi import FastAPI, status , Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from router.admin_router import admin_router 
from router.manager_router import manager_router 
from router.emp_router import emp_router
from models.index_model import JoiningRequest 
from config.db_connection import get_db
from config.password_security import hash_password
from schema.schemas import DataFormatter

from logging_config import setup_logging
import logging

setup_logging()

app = FastAPI()

# Project start announcement
logging.info("FastAPI project initialized. Project is ready to accept requests.")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"),name = "static")

@app.get("/",response_class=HTMLResponse)
async def index_page(request: Request):

    """    
    Index Page [Welcome Page]

    Args:
        request (Request): Holds information of incomming HTTP request.
        
    Returns:
        [text/html] :index.html
    """
    
    logging.info("Accessed Index page")
    return templates.TemplateResponse("index.html",{"request": request})

@app.get(r"/registration_form")
def register_as_employee_form(request: Request, db = Depends(get_db)):

    """    
    Employee and Manager Registration Form

    Args:
        request (Request): Holds information of incomming HTTP request.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        [text/html] :joining_request.html

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logging.info("Accessed registration form page")

    sql, cursor = db
    sql_query_to_fetch_all_admin = f"""SELECT DISTINCT admin_id , admin_name FROM admin;"""
    logging.debug(f"SQL Query for Fetching the Admins: {sql_query_to_fetch_all_admin} ")
    try:
        cursor.execute(sql_query_to_fetch_all_admin)
        table_data = cursor.fetchall()
        logging.info("Admin Details fetched Successfully")

        data_formatter = DataFormatter()
        data_entries = data_formatter.dictionary_list(table_data=table_data, table_column=["admin_id","admin_name"])
        logging.info("Data formatted successfully. Ready for sending it to Webpage")
    except Exception as e:
        logging.error(f"Error occurred while fetching admin data: {e}")
        HTTPException(status_code=500 , detail="Unable render the registration Form")
    else:
        return templates.TemplateResponse("joining_request.html",{"request": request, "data_entries":data_entries})

@app.post(r"/registration_form", response_class=JSONResponse)
def register_as_employee( request: Request, joining_request:JoiningRequest, db = Depends(get_db)):

    """    
    Employee Registration Request is addressed Here.

    Args:
        request (Request): Holds information of incomming HTTP request.
        joining_request (JoiningRequest) : Holds the Data of Submitted Registration Form.
        db (Tuple) : Holds (sql, cursor) for executing sql query.

    Returns:
        json :{"message": "Joining Record Saved Successfully"}

    Raises:
        HTTPException [status_code = 500] : Error executing query.
    """

    logging.info("Received registration form submission Request")
    sql, cursor = db
    print(joining_request)
    sql_query_to_register_employee = f"""
    INSERT INTO joining_request (id, name, password, emp_type, admin_id, email, mobile, gender, date_of_joining, status)
    VALUES 
    ('{joining_request.id}',
    '{joining_request.name}', 
    '{hash_password(joining_request.password)}',   
    '{joining_request.emp_type}',
    '{joining_request.admin_id}',
    '{joining_request.email}',
    '{joining_request.mobile}',
    '{joining_request.gender}',
    '{joining_request.date_of_joining}',
    'Pending'
    )
    """
    logging.debug(f"SQL Query to save the Joining request of the User: {sql_query_to_register_employee}")
    try:
        cursor.execute("START TRANSACTION ;")
        cursor.execute(sql_query_to_register_employee)
        sql.commit()
        logging.info(f"Employee registration with id : {joining_request.id} hsa been saved successfully")
    except Exception as e:
        sql.rollback()
        logging.error(f"Error occurred while saving employee registration record having id : {joining_request.id}: {e}")
        raise HTTPException(status_code = 500 , detail = "Error occurred while saving employee registration record")
    else:
        redirect_url = request.url_for("register_as_employee_form")
        return JSONResponse(content = {"message": "Joining Record Saved Successfully"})

app.include_router(admin_router)

app.include_router(manager_router)

app.include_router(emp_router)