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

@pytest.mark.order(4)
def test_login_page_of_admin(client):
    response = client.get("/admin_login")
    assert response.status_code == 200
    
@pytest.mark.order(5)
def test_admin_login_processing(client):
    response = client.post("/admin_login_data", json = {
        "username": "Test_ADM0",
        "password": "Test_Password0"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Login Successful"}
   
    response = client.post("/admin_login_data", json = {
        "username": "Test_ADM",
        "password": "Test_Passwd0"
    })
    assert response.status_code == 401
    assert response.json() == {"detail":"Invalid username or password"}
                
@pytest.mark.order(6)
def test_admin_home(client):
    response = client.get("/admin_home")
    assert response.status_code == 200
 

@pytest.mark.order(7)
def test_joining_request(client):
    response = client.get("/joining_request", headers= {"admin_id":"Test_ADM0"})
    assert response.status_code == 200
       
@pytest.mark.order(8)
def test_accept_joining_request(client):
    for x in range(1,14):
        response = client.post("/accept_joining_request", json={
            "id": "Test_EMP00%s" % x,
            "emp_type": "Employee"
        })
        assert response.status_code == 200
        assert response.json() == {"message":"Employee Joining Request was successfully Accepted"}
    
    for c in range(1,3):
        response = client.post("/accept_joining_request", json={
            "id": "Test_MGR00%s" % c,
            "emp_type": "Manager"
        })
        assert response.status_code == 200
        assert response.json() == {"message":"Employee Joining Request was successfully Accepted"}

    response = client.post("/accept_joining_request", json={
            "id": "Test_EMP001",
            "emp_type": "Employee"
        })
    assert response.status_code == 500
    assert response.json() == {"detail":"An error occurred while processing the request"}

@pytest.mark.order(9)
def test_reject_joining_request(client):
    response = client.post("/reject_joining_request", json={
        "id": "Test_EMP000"
    })
    assert response.status_code == 200
    assert response.json() ==  {"message":"Employee Joining Request was Rejected"}
    
    response = client.post("/reject_joining_request", json={
        "id": "Test_MGR000"
    })
    assert response.status_code == 200
    assert response.json() ==  {"message":"Employee Joining Request was Rejected"}

@pytest.mark.order(10)
def test_create_project_form(client):
    response = client.get("/create_project_form")
    assert response.status_code == 200
       
@pytest.mark.order(11)
def test_create_project_form_processing(client):
    response = client.post("/create_project_form_processing", json={
        "project_id": "Test_PROJ001",
        "project_name": "Test_Project001",
        "dead_line": "24-11-20",
        "description": "This is project For Test Purpose",
        "assign_to": "Test_MGR001",
        "admin_id": "Test_ADM0"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"A Project has been created successfully"}
    
    response = client.post("/create_project_form_processing", json={
        "project_id": "Test_PROJ002",
        "project_name": "Test_Project002",
        "dead_line": "2030-12-20",
        "description": "This is project For Test Purpose",
        "assign_to": "Later",
        "admin_id": "Test_ADM0"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"A Project has been created successfully"}
    
    response = client.post("/create_project_form_processing", json={
        "project_id": "Test_PROJ003",
        "project_name": "Test_Project003",
        "dead_line": "2030-12-20",
        "description": "This is project For Test Purpose",
        "assign_to": "Test_MGR002",
        "admin_id": "Test_ADM0"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"A Project has been created successfully"}
    
    response = client.post("/create_project_form_processing", json={
        "project_id": "Test_PROJ004",
        "project_name": "Test_Project004",
        "dead_line": "2030-12-20",
        "description": "This is project For Test Purpose",
        "assign_to": "Later",
        "admin_id": "Test_ADM0"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"A Project has been created successfully"}

    response = client.post("/create_project_form_processing", json={
        "project_id": "Test_PROJ004",
        "project_name": "Test_Project004",
        "dead_line": "2030-12-20",
        "description": "This is project For Test Purpose",
        "assign_to": "Later",
        "admin_id": "Test_ADM0"
    })
    assert response.status_code == 500
    assert response.json() == {"detail":"An error occurred while creating new project"}



@pytest.mark.order(12)
def test_view_all_project(client):
    response = client.get("/admin_view_all_project")
    assert response.status_code == 200

@pytest.mark.order(13)
def test_update_employee_skill(client):
    response = client.get("/update_employee_skill")
    assert response.status_code == 200
    

@pytest.mark.order(14)
def test_add_employee_skill(client):
    response = client.put("/add_employee_skill", json = { 
        "emp_id":"Test_EMP004",
        "skills":"Python , Spark , Java"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"skill added successfully"}

@pytest.mark.order(15)
def test_replace_employee_skill(client):
    response = client.put("/replace_employee_skill", json = { 
        "emp_id":"Test_EMP005",
        "skills":"Python , Spark , Java"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Employee skill replaced Successfully"}

@pytest.mark.order(16)
def test_fetch_all_employees_and_project_for_admin(client):
    response = client.get("/admin_view_all")
    assert response.status_code == 200


@pytest.mark.order(17)
def test_assign_project(client):
    response = client.get("/assign_project")
    assert response.status_code == 200

@pytest.mark.order(18)
def test_assign_project_to_manager(client):
    response = client.post("/assign_manager_a_project", json={
        "manager_id": "Test_MGR001",
        "project_id": "Test_PROJ002"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"A project is assigned to manager"}

    response = client.post("/assign_manager_a_project", json={
        "manager_id": "Test_MGR002",
        "project_id": "Test_PROJ004"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"A project is assigned to manager"}

@pytest.mark.order(19)
def test_assign_project_to_employees(client):
    response = client.post("/assign_employee_a_project", json={
        "emp_id": "Test_EMP001",
        "project_id": "Test_PROJ001"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"A project is assigned to employee"}
    
    response = client.post("/assign_employee_a_project", json={
        "emp_id": "Test_EMP002",
        "project_id": "Test_PROJ002"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"A project is assigned to employee"}

    response = client.post("/assign_employee_a_project", json={
        "emp_id": "Test_EMP003",
        "project_id": "Test_PROJ003"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"A project is assigned to employee"}

    response = client.post("/assign_employee_a_project", json={
        "emp_id": "Test_EMP004",
        "project_id": "Test_PROJ004"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"A project is assigned to employee"}

    
@pytest.mark.order(26)
def test_manager_request(client):
    response = client.get("/manager_request")
    assert response.status_code == 200
   
@pytest.mark.order(27)
def test_accept_manager_request(client):
    response = client.post("/accept_manager_request", json={
        "emp_id": "Test_EMP005",
        "project_id": "Test_PROJ001",
        "manager_id": "Test_MGR001"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Manager request Accepted"}

    response = client.post("/accept_manager_request", json={
        "emp_id": "Test_EMP006",
        "project_id": "Test_PROJ002",
        "manager_id": "Test_MGR001"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Manager request Accepted"}

    response = client.post("/accept_manager_request", json={
        "emp_id": "Test_EMP007",
        "project_id": "Test_PROJ003",
        "manager_id": "Test_MGR002"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Manager request Accepted"}

    response = client.post("/accept_manager_request", json={
        "emp_id": "Test_EMP008",
        "project_id": "Test_PROJ004",
        "manager_id": "Test_MGR002"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Manager request Accepted"}

@pytest.mark.order(28)
def test_reject_manager_request(client):
    response = client.put("/reject_manager_request", json={
        "emp_id": "Test_EMP009",
        "project_id": "Test_PROJ001",
        "manager_id": "Test_MGR001"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Manager request Rejected"}

    response = client.put("/reject_manager_request", json={
        "emp_id": "Test_EMP0010",
        "project_id": "Test_PROJ002",
        "manager_id": "Test_MGR001"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Manager request Rejected"}

    response = client.put("/reject_manager_request", json={
        "emp_id": "Test_EMP0011",
        "project_id": "Test_PROJ003",
        "manager_id": "Test_MGR002"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Manager request Rejected"}

    response = client.put("/reject_manager_request", json={
        "emp_id": "Test_EMP0012",
        "project_id": "Test_PROJ004",
        "manager_id": "Test_MGR002"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Manager request Rejected"}


@pytest.mark.order(29)
def test_unassign_project(client):
    response = client.get("/unassign_project")
    assert response.status_code == 200
 
@pytest.mark.order(30)
def test_unassign_employee_from_project(client):
    response = client.put("/unassign_employee_from_project", json={
        "emp_id": "Test_EMP006"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Employee was unassigned from a Project"}

@pytest.mark.order(31)
def test_unassign_manager_from_project(client):
    response = client.put("/unassign_manager_from_project", json={
        "manager_id": "Test_MGR001",
        "project_id": "Test_PROJ002"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Manager was unassigned from a Project"}

    response = client.put("/unassign_manager_from_project", json={
        "manager_id": "Test_MGR002",
        "project_id": "Test_PROJ004"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"Manager was unassigned from a Project"}

@pytest.mark.order(32)
def test_assign_unassign_project_to_manager(client):
    response = client.post("/assign_manager_a_project", json={
        "manager_id": "Test_MGR001",
        "project_id": "Test_PROJ004"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"A project is assigned to manager"}

    
    response = client.post("/assign_manager_a_project", json={
        "manager_id": "Test_MGR002",
        "project_id": "Test_PROJ002"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"A project is assigned to manager"}

@pytest.mark.order(35)
def test_manager_project_completion_request(client):
    response = client.get("/manager_request_to_complete_project")
    assert response.status_code == 200

@pytest.mark.order(36)
def test_reject_completion_of_project_three(client):
    response = client.put("/reject_completion_of_project?project_id=Test_PROJ003")
    assert response.status_code == 200
    assert response.json() == {"message":"Project status set to Review"}

@pytest.mark.order(37)
def test_approve_completion_of_project_one(client):
    response = client.delete("/approve_completion_of_project?project_id=Test_PROJ001")
    assert response.status_code == 200
    assert response.json() == {"message":"Project Completed"}


@pytest.mark.order(46)
def test_remove_worker(client):
    response = client.get("/remove_workers")
    assert response.status_code == 200
    


@pytest.mark.order(47)
def test_remove_manager(client):
    for num in range(1,2):
        response = client.delete(f"/remove_manager?manager_id=Test_MGR00{num}")
        assert response.status_code == 200
        assert response.json() == {"message":"Manager has been removed successfully"}
        
@pytest.mark.order(48)
def test_remove_employee(client):
    for num in range(1,13,2):
        response = client.delete(f"/remove_employee?emp_id=Test_EMP00{num}")
        assert response.status_code == 200
        assert response.json() == {"message":"Employee has been removed successfully"}



@pytest.mark.order(49)
def test_assign_project_of_terminated_manager(client):
    response = client.post("/assign_manager_a_project", json={
        "manager_id": "Test_MGR002",
        "project_id": "Test_PROJ004"
    })
    assert response.status_code == 200
    assert response.json() == {"message":"A project is assigned to manager"}

@pytest.mark.order(51)
def test_approve_completion_of_project(client):
    response = client.delete("/approve_completion_of_project?project_id=Test_PROJ003")
    assert response.status_code == 200
    assert response.json() == {"message":"Project Completed"}

    response = client.delete("/approve_completion_of_project?project_id=Test_PROJ002")
    assert response.status_code == 200
    assert response.json() == {"message":"Project Completed"}

    response = client.delete("/approve_completion_of_project?project_id=Test_PROJ004")
    assert response.status_code == 200
    assert response.json() == {"message":f"Project Completed"}


@pytest.mark.order( 52)
def test_admin_login(client):
    response = client.get("/admin_logout")
    assert response.status_code == 200
    assert response.json() == {"message": "Admin successfully Logout"}
   
# @pytest.mark.order(52)
# def test_remove_all(client):
#     response = client.delete(f"/remove_all?admin_id=Test_ADM0")
#     assert response.status_code == 200
#     assert response.json() == {"message":"Everything Removed Successfully"}
    