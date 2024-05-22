"""
[main.py] : Starting of app
"""
from fastapi import FastAPI, status 
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from router.admin_router import admin_router 
from router.manager_router import manager_router 
from router.emp_router import emp_router
from models.index_model import JoiningRequest 
from config.db_connection import sql , cursor
from schema.schemas import DataFormatter
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"),name = "static")

@app.get("/",response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})

@app.get(r"/registration_form")
def register_as_employee_form(request: Request):
    sql_query_to_fetch_all_admin = f"""SELECT DISTINCT admin_id , admin_name FROM admin;"""
    try:
        cursor.execute(sql_query_to_fetch_all_admin)
        table_data = cursor.fetchall()
        data_formatter = DataFormatter()
        data_entries = data_formatter.dictionary_list(table_data=table_data, table_column=["admin_id","admin_name"])
    except Exception as e:
        print(e)
    else:
        return templates.TemplateResponse("joining_request.html",{"request": request, "data_entries":data_entries})

@app.post(r"/registration_form_submission")
def register_as_employee( request: Request, joining_request:JoiningRequest):
    print(joining_request)
    sql_query_to_register_employee = f"""
    INSERT INTO joining_request (id, name, password, emp_type, admin_id, email, mobile, gender, date_of_joining, status)
    VALUES 
    ('{joining_request.id}',
    '{joining_request.name}', 
    '{joining_request.password}',   
    '{joining_request.emp_type}',
    '{joining_request.admin_id}',
    '{joining_request.email}',
    '{joining_request.mobile}',
    '{joining_request.gender}',
    '{joining_request.date_of_joining}',
    'Pending'
    )
    """
    try:
        cursor.execute(sql_query_to_register_employee)
        sql.commit()
    except Exception as e:
        print(e)
    else:
        redirect_url = request.url_for("register_as_employee_form")
        return RedirectResponse(redirect_url, status.HTTP_303_SEE_OTHER)

app.include_router(admin_router)

app.include_router(manager_router)

app.include_router(emp_router)