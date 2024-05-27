import sys,os
sys.path.append(os.path.join(os.path.abspath('..'),"app"))
print(sys.path)
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app  # assuming your FastAPI instance is in main.py

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.order(31)
def test_employee_login(client):
    response = client.get("/employee_login")
    assert response.status_code == 200

@pytest.mark.order(32)
def test_employee_login(client):
    for num in range(1,7):
        response = client.post("/employee_login_data", json={
            "username": "Test_EMP00%s" % num,
            "password": "Password%s"% num
        })
        assert response.status_code == 200
        assert response.json() == {"message":"Login Successful"}
    

@pytest.mark.order(33 )
def test_employee_home(client):
    response = client.get("/employee_home")
    assert response.status_code == 200

@pytest.mark.order(34 )
def test_fetch_all_workers_for_project(client):
    response = client.get("/employee_for_project")
    assert response.status_code == 200
   
@pytest.mark.order(35 )
def test_update_skills_as_employee(client):
    response = client.get("/update_skills_as_employee")
    assert response.status_code == 200
 
@pytest.mark.order(36 )
def test_add_skill(client):
    response = client.put("/add_skill", json={
        "emp_id": "Test_EMP001",
        "skills": "Python, Java, Spark"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Skill added Successfully"}

@pytest.mark.order(37 )
def test_replace_skill(client):
    response = client.put("/replace_skill", json={
        "emp_id": "Test_EMP001",
        "skills": "Java"
    })
    assert response.status_code == 200
    assert response.json() ==  {"message":"Skill replaced Successfully"}

@pytest.mark.order(38 )
def test_employee_project_details(client):
    response = client.get("/employee_project_details")
    assert response.status_code == 200