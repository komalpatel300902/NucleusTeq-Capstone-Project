import sys,os
sys.path.append(os.path.join(os.path.abspath('..'),"app"))
print(sys.path)
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import MagicMock, patch
from app.main import app
import datetime
tommorow_date = datetime.date.today()+ datetime.timedelta(days= 1)
tommorow_date = tommorow_date.strftime("%Y-%m-%d")

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.order(0)
def test_admin_access_without_login(client):
    response = client.get("/admin_home")
    assert response.status_code == 401
    response.json() == {"detail":"Unauthoroised User"}

@pytest.mark.order(0)
def test_manager_access_without_login(client):
    response = client.get("/manager_home")
    assert response.status_code == 401
    response.json() == {"detail":"Unauthoroised User"}

@pytest.mark.order(0)
def test_employee_access_without_login(client):
    response = client.get("/employee_home")
    assert response.status_code == 401
    response.json() == {"detail":"Unauthoroised User"}




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
            "/registration_form",
            json={
                "id": "Test_MGR00%s" % num,
                "name": "Manager%s" % num,
                "password": "Password%s" % num,
                "emp_type": "Manager",
                "admin_id": "Test_ADM0",
                "email": "manager%s@nucleusteq.com" % num,
                "mobile": "6263218976",
                "gender": "Male",
                "date_of_joining": tommorow_date
            }
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Joining Record Saved Successfully"}  # Ensure it redirects to the form
    for num in range(14):
        response = client.post(
            "/registration_form",
            json={
                "id": "Test_EMP00%s" % num,
                "name": "Employee%s" % num,
                "password": "Password%s" % num,
                "emp_type": "Employee",
                "admin_id": "Test_ADM0",
                "email": "employee%s@nucleusteq.com" % num,
                "mobile": "6263211233",
                "gender": "Male",
                "date_of_joining": tommorow_date
            }
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Joining Record Saved Successfully"}  # Ensure it redirects to the form
    
    # Checking Date
    response = client.post(
            "/registration_form",
            json={
                "id": "Test_EMP0014",
                "name": "Employee14",
                "password": "Password14",
                "emp_type": "Employee",
                "admin_id": "Test_ADM0",
                "email": "employee14@nucleusteq.com",
                "mobile": "6263212321",
                "gender": "Male",
                "date_of_joining": "2024-05-01"
            }
        )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail": "Date must be greater than yesterday's date."}


    """Checking Mobile Number [ Excedding 10 digit]"""
    response = client.post(
            "/registration_form",
            json={
                "id": "Test_EMP0014",
                "name": "Employee14",
                "password": "Password14",
                "emp_type": "Employee",
                "admin_id": "Test_ADM0",
                "email": "employee14@nucleusteq.com",
                "mobile": "62632123219", # 11 digit
                "gender": "Male",
                "date_of_joining": "2024-05-01"
            }
        )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail" : "Length of mobile number must be 10"}
    """Checking Mobile Number [Less than 10 Digit]"""
    response = client.post(
            "/registration_form",
            json={
                "id": "Test_EMP0014",
                "name": "Employee14",
                "password": "Password14",
                "emp_type": "Employee",
                "admin_id": "Test_ADM0",
                "email": "employee14@nucleusteq.com",
                "mobile": "6262321", # 7 digit
                "gender": "Male",
                "date_of_joining": "2024-05-01"
            }
        )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == { "detail":"Length of mobile number must be 10"}
    """Checking Mobile Number [alpha numeric]"""
    response = client.post(
            "/registration_form",
            json={
                "id": "Test_EMP0014",
                "name": "Employee14",
                "password": "Password14",
                "emp_type": "Employee",
                "admin_id": "Test_ADM0",
                "email": "employee14@nucleusteq.com",
                "mobile": "6262321abc", # Alphanumeric
                "gender": "Male",
                "date_of_joining": "2024-05-01"
            }
        )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail": 'Mobile number must be digit'}
    # [Password Length less than 8]
    response = client.post(
            "/registration_form",
            json={
                "id": "Test_EMP0014",
                "name": "Employee14",
                "password": "Passwd1",
                "emp_type": "Employee",
                "admin_id": "Test_ADM0",
                "email": "employee14@nucleusteq.com",
                "mobile": "6263212321",
                "gender": "Male",
                "date_of_joining": "2024-05-01"
            }
        )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail":'Length of password must be > 8 and  < 30'}
    #  password > 30
    response = client.post(
            "/registration_form",
            json={
                "id": "Test_EMP0014",
                "name": "Employee14",
                "password": "Passwdsqwertyuiopasdfghjklzxcvbnmqazwsx123",
                "emp_type": "Employee",
                "admin_id": "Test_ADM0",
                "email": "employee14@nucleusteq.com",
                "mobile": "6263212321",
                "gender": "Male",
                "date_of_joining": "2024-05-01"
            }
        )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail": 'Length of password must be > 8 and  < 30'}

    # checking password[for Upper Case]
    response = client.post(
            "/registration_form",
            json={
                "id": "Test_EMP0014",
                "name": "Employee14",
                "password": "password14",
                "emp_type": "Employee",
                "admin_id": "Test_ADM0",
                "email": "employee14@nucleusteq.com",
                "mobile": "6263212321",
                "gender": "Male",
                "date_of_joining": "2024-05-01"
            }
        )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail": 'Password must contain at least one uppercase letter'}
    #[For Lower Case]
    response = client.post(
            "/registration_form",
            json={
                "id": "Test_EMP0014",
                "name": "Employee14",
                "password": "PASSWORD14",
                "emp_type": "Employee",
                "admin_id": "Test_ADM0",
                "email": "employee14@nucleusteq.com",
                "mobile": "6263212321",
                "gender": "Male",
                "date_of_joining": "2024-05-01"
            }
        )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail": 'Password must contain at least one lowercase letter'}
    # [For Numeric]
    response = client.post(
            "/registration_form",
            json={
                "id": "Test_EMP0014",
                "name": "Employee14",
                "password": "Password",
                "emp_type": "Employee",
                "admin_id": "Test_ADM0",
                "email": "employee14@nucleusteq.com",
                "mobile": "6263212321",
                "gender": "Male",
                "date_of_joining": "2024-05-01"
            }
        )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail":'Password must contain at least one digit'}
    
    """Checking Email [Domain]"""
    response = client.post(
            "/registration_form",
            json={
                "id": "Test_EMP0014",
                "name": "Employee14",
                "password": "Password14",
                "emp_type": "Employee",
                "admin_id": "Test_ADM0",
                "email": "employee14@gmail.com",
                "mobile": "6263212321",
                "gender": "Male",
                "date_of_joining": "2024-05-01"
            }
        )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail": 'email domain must belong to Organization'}
    # Without Error
    response = client.post(
            "/registration_form",
            json={
                "id": "Test_EMP0014",
                "name": "Employee14",
                "password": "Password14",
                "emp_type": "Employee",
                "admin_id": "Test_ADM0",
                "email": "employee14@nucleusteq.com",
                "mobile": "6263212321",
                "gender": "Male",
                "date_of_joining": tommorow_date
            }
        )
    assert response.status_code == status.HTTP_200_OK

    # [For except Block : Passing Duplicate Entry]
    response = client.post(
            "/registration_form",
            json={
                "id": "Test_MGR001",
                "name": "Manager",
                "password": "Password100",
                "emp_type": "Manager",
                "admin_id": "Test_ADM0",
                "email": "manager100@nucleusteq.com",
                "mobile": "6263218976",
                "gender": "Binary",
                "date_of_joining": tommorow_date
            }
    )
    assert response.status_code == 500
    assert response.json() == {"detail" : "Error occurred while saving employee registration record"}
    