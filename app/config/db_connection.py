"""[sql , cursor]
This module is used to connect database
"""

import  mysql.connector as mysql_connector

def get_db():
    try:
        sql = mysql_connector.connect(host = "localhost", user = "root",passwd = "",database = "emp_management_db")
        cursor = sql.cursor()
        yield (sql,cursor)
    except Exception as e:
        print("Unable To connect the SQl Database.")
