import sys,os
sys.path.append(os.path.join(os.path.abspath('..'),"app"))
print(sys.path)
import pytest
from fastapi.testclient import TestClient
from main import app

# @pytest.fixture
# def client():
#     return TestClient(app)

# @pytest.mark.run()
# def test_joining_request(client):
#     response = client.get("/joining_request", headers= {"admin_id":"Test_ADM000"})
#     assert response.status_code == 200
    
       
