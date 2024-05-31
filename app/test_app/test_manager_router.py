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

@pytest.mark.order(20)
def test_manager_login(client):
    response = client.get("/manager_login")
    assert response.status_code == 200
    
@pytest.mark.order(21 )
def test_manager_home(client):
    response = client.get("/manager_home")
    assert response.status_code == 200
   
@pytest.mark.order(22)
def test_get_all_employees_and_project(client):
    response = client.get("/comprehensive_info")
    assert response.status_code == 200
   
@pytest.mark.order(23)
def test_get_filtered_employees(client):
    response = client.get("/filtered_employee")
    assert response.status_code == 200

@pytest.mark.order(24)
def test_request_employee(client):
    response = client.post("/request_for_employee", json={
        "emp_id": "Test_EMP005",
        "project_id": "Test_PROJ001",
        "manager_id":"Test_MGR001"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Request for employee sent Successfully"}
    
    response = client.post("/request_for_employee", json={
        "emp_id": "Test_EMP006",
        "project_id": "Test_PROJ002",
        "manager_id":"Test_MGR001"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Request for employee sent Successfully"}

    response = client.post("/request_for_employee", json={
        "emp_id": "Test_EMP007",
        "project_id": "Test_PROJ003",
        "manager_id":"Test_MGR002"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Request for employee sent Successfully"}


    response = client.post("/request_for_employee", json={
        "emp_id": "Test_EMP008",
        "project_id": "Test_PROJ004",
        "manager_id":"Test_MGR002"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Request for employee sent Successfully"}

@pytest.mark.order(25)
def test_project_manager_have(client):
    response = client.get("/projects_manager_have")
    assert response.status_code == 200


@pytest.mark.order(33)
def test_update_project_status(client):
    response = client.get("/update_project_status")
    assert response.status_code == 200


@pytest.mark.order(34)
def test_update_project_status(client):
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

    
@pytest.mark.order(50)
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

    
    




