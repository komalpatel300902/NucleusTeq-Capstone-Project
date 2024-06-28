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

@pytest.mark.order(36)
def test_login_page_of_manager(client):
    response = client.get("/manager_login")
    assert response.status_code == 200
    
@pytest.mark.order(37)
def test_manager_login_processing(client):
    response = client.post("/manager_login", json = {
        "username": "Test_MGR001",
        "password": "Password1"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Login Successful"}
   
    response = client.post("/manager_login", json = {
        "username": "Test_ADM",
        "password": "Test_Passwd0"
    })
    assert response.status_code == 401
    assert response.json() == {"detail":"Invalid username or password"}
     
@pytest.mark.order(38)
def test_manager_home(client):
    response = client.get("/manager_home")
    assert response.status_code == 200
   
@pytest.mark.order(39)
def test_get_all_employees_and_project(client):
    response = client.get("/comprehensive_info")
    assert response.status_code == 200
   
@pytest.mark.order(40)
def test_get_filtered_employees(client):
    response = client.get("/filtered_employee")
    assert response.status_code == 200

@pytest.mark.order(41)
def test_request_employee(client):
    response = client.post("/filtered_employee", json={
        "emp_id": "Test_EMP005",
        "project_id": "Test_PROJ001",
        "manager_id":"Test_MGR001"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Request for employee sent Successfully"}
    
    response = client.post("/filtered_employee", json={
        "emp_id": "Test_EMP006",
        "project_id": "Test_PROJ002",
        "manager_id":"Test_MGR001"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Request for employee sent Successfully"}

    response = client.post("/filtered_employee", json={
        "emp_id": "Test_EMP007",
        "project_id": "Test_PROJ003",
        "manager_id":"Test_MGR002"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Request for employee sent Successfully"}


    response = client.post("/filtered_employee", json={
        "emp_id": "Test_EMP008",
        "project_id": "Test_PROJ004",
        "manager_id":"Test_MGR002"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Request for employee sent Successfully"}

    response = client.post("/filtered_employee", json={
        "emp_id": "Test_EMP008",
        "project_id": "Test_PROJ001",
        "manager_id":"Test_MGR002"
    })
    assert response.status_code == 422
    assert response.json() == {"detail":"Employee does not have the skill for the project"}

@pytest.mark.order(42)
def test_project_manager_have(client):
    response = client.get("/projects_manager_have")
    assert response.status_code == 200


@pytest.mark.order(54)
def test_request_admin_to_unassing_emp_from_project_page(client):
    response = client.get("/request_admin_to_unassign_emp_from_project")
    assert response.status_code == 200

@pytest.mark.order(55)
def test_request_admin_to_unassing_emp_from_project(client):
    response = client.post("/request_admin_to_unassign_emp_from_project", json = {
        "emp_id": "Test_EMP005",
        "project_id": "Test_PROJ001",
        "manager_id": "Test_MGR001"
    })

    assert response.status_code == 200
    assert response.json() == {"message":"Request for employee removal sent Successfully"}

    response = client.post("/request_admin_to_unassign_emp_from_project", json = {
        "emp_id": "Test_EMP006",
        "project_id": "Test_PROJ002",
        "manager_id": "Test_MGR001"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Request for employee removal sent Successfully"}

    response = client.post("/request_admin_to_unassign_emp_from_project", json = {
        "emp_id": "Test_EMP007",
        "project_id": "Test_PROJ003",
        "manager_id": "Test_MGR002"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Request for employee removal sent Successfully"}

    response = client.post("/request_admin_to_unassign_emp_from_project", json = {
        "emp_id": "Test_EMP008",
        "project_id": "Test_PROJ004",
        "manager_id": "Test_MGR002"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Request for employee removal sent Successfully"}


@pytest.mark.order(71)
def test_update_the_project_status_page(client):
    response = client.get("/update_project_status")
    assert response.status_code == 200


@pytest.mark.order(72)
def test_update_the_status_of_project(client):
    response = client.put("/update_project_status", json = {"manager_id":"Test_MGR001", "project_id":"Test_PROJ001","status":"In Progress"})
    assert response.status_code == 200
    assert response.json() == {"message": "Project status Updated Successfully"}
    
    response = client.put("/update_project_status", json = {"manager_id":"Test_MGR001", "project_id":"Test_PROJ001","status":"Review"})
    assert response.status_code == 200
    assert response.json() == {"message": "Project status Updated Successfully"}
    
    response = client.put("/update_project_status", json = {"manager_id":"Test_MGR001", "project_id":"Test_PROJ001","status":"Completed"})
    assert response.status_code == 200
    assert response.json() == {"message": "Project status Updated Successfully"}
    

    response = client.put("/update_project_status", json = {"manager_id":"Test_MGR002", "project_id":"Test_PROJ003","status":"Completed"})
    assert response.status_code == 200
    assert response.json() == {"message": "Project status Updated Successfully"}

    
@pytest.mark.order(116)
def test_update_project_status(client):
    
    response = client.put("/update_project_status", json = {"manager_id":"Test_MGR002", "project_id":"Test_PROJ002","status":"Completed"})
    assert response.status_code == 200
    assert response.json() == {"message": "Project status Updated Successfully"}
    
    response = client.put("/update_project_status", json = {"manager_id":"Test_MGR002", "project_id":"Test_PROJ003","status":"Completed"})
    assert response.status_code == 200
    assert response.json() == {"message": "Project status Updated Successfully"}
    

    response = client.put("/update_project_status", json = {"manager_id":"Test_MGR002", "project_id":"Test_PROJ004","status":"Completed"})
    assert response.status_code == 200
    assert response.json() == {"message": "Project status Updated Successfully"}

@pytest.mark.order(210)
def test_manger_logout(client):
    response = client.post("/manager_logout")
    assert response.status_code == 200
    assert response.json() == {"message": "Manager Successfully Logout"}

    
    




