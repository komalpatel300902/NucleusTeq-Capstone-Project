"""[sql , cursor]
This module is used to connect database
"""

import  mysql.connector as mysql_connector
try:
    sql = mysql_connector.connect(host = "localhost", user = "root",passwd = "",database = "emp_management_db")
    cursor = sql.cursor()
except Exception as e:
    print(e)
else:
    print("connected Successfully !!!")

