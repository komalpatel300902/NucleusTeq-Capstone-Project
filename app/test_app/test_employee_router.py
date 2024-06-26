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

@pytest.mark.order(24)
def test_login_page_of_employee(client):
    response = client.get("/employee_login")
    assert response.status_code == 200

@pytest.mark.order(25)
def test_employee_login(client):
    for num in range(1,7):
        response = client.post("/employee_login", json={
            "username": "Test_EMP00%s" % num,
            "password": "Password%s"% num
        })
        assert response.status_code == 200
        assert response.json() == {"message":"Login Successful"}
    
        response = client.post("/employee_login",json = {
        "username": "Test_ADM",
        "password": "Test_Passwd0"
        })
        assert response.status_code == 401
        assert response.json() == {"detail":"Invalid username or password"}
        
@pytest.mark.order(26)
def test_employee_home(client):
    response = client.get("/employee_home")
    assert response.status_code == 200

@pytest.mark.order(27)
def test_fetch_all_workers_for_project(client):
    response = client.get("/all_colleague")
    assert response.status_code == 200
   
@pytest.mark.order(28)
def test_update_skills_as_employee(client):
    response = client.get("/update_skills_as_employee")
    assert response.status_code == 200
 
@pytest.mark.order(29)
def test_add_skill(client):
    response = client.put("/add_skill", json={
        "emp_id": "Test_EMP001",
        "skills": "Python, Java, Spark"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Skill added Successfully"}

@pytest.mark.order(30)
def test_replace_skill(client):
    skills = ["pyspark","fastapi","django","flask"]
    for a in range(1,13):
        response = client.put("/replace_skill", json={
            "emp_id": "Test_EMP00%s"% a,
            "skills": skills[a%4]
        })
        assert response.status_code == 200
        assert response.json() ==  {"message":"Skill replaced Successfully"}

@pytest.mark.order(98)
def test_employee_project_details(client):
    response = client.get("/employee_project_details")
    assert response.status_code == 200

@pytest.mark.order(211)
def test_employee_logout(client):
    response = client.post("/employee_logout")
    assert response.status_code == 200
    assert response.json() == {"message": "User Successfully Logout"}
