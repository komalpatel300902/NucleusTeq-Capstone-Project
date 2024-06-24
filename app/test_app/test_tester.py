# import sys,os
# sys.path.append(os.path.join(os.path.abspath('..'),"app"))
# print(sys.path)
# import pytest
# from fastapi.testclient import TestClient
# from main import app


# @pytest.mark.order(52)
# def test_remove_all(client):
#     response = client.delete(f"/remove_all?admin_id=Test_ADM0")
#     assert response.status_code == 200
#     assert response.json() == {"message":"Everything Removed Successfully"}

import datetime
if __name__ == "__main__":
    tommorow_date = datetime.date.today()+ datetime.timedelta(days= 1)
    tommorow_date = tommorow_date.strftime("%Y-%m-%d")
    print(tommorow_date)