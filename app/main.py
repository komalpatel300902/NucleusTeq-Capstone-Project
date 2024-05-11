"""
[main.py] : Starting of app
"""
from fastapi import FastAPI, status 
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import HTMLResponse
from router.admin_router import admin_router 
from router.manager_router import manager_router 
from router.emp_router import emp_router

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"),name = "static")

@app.get("/",response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})

@app.post(r"/login")
def login() -> None: ...

@app.post(r"/register")
def regester_as_employee() -> None: ...

app.include_router(admin_router)

app.include_router(manager_router)

app.include_router(emp_router)