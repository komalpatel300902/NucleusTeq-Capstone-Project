import sys,os
sys.path.append(os.path.join(os.path.abspath('..'),"app"))
print(sys.path)
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.order(1)
def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200

@pytest.mark.order(2)  
def test_register_as_employee_form(client):
    response = client.get("/registration_form")
    assert response.status_code == 200

@pytest.mark.order(3) 
def test_register_as_employee_submission(client):
    for num in range(3):
        response = client.post(
            "/registration_form_submission",
            json={
                "id": "Test_MGR00%s" % num,
                "name": "Manager%s" % num,
                "password": "Password%s" % num,
                "emp_type": "Manager",
                "admin_id": "Test_ADM0",
                "email": "manager%s@example.com" % num,
                "mobile": "626321",
                "gender": "Male",
                "date_of_joining": "2024-05-01"
            }
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Joining Record Saved Successfully"}  # Ensure it redirects to the form
    for num in range(14):
        response = client.post(
            "/registration_form_submission",
            json={
                "id": "Test_EMP00%s" % num,
                "name": "Employee%s" % num,
                "password": "Password%s" % num,
                "emp_type": "Employee",
                "admin_id": "Test_ADM0",
                "email": "employee%s@example.com" % num,
                "mobile": "626321",
                "gender": "Male",
                "date_of_joining": "2024-05-01"
            }
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Joining Record Saved Successfully"}  # Ensure it redirects to the form

