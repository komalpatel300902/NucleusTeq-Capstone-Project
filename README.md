## Introduction

Welcome Everyone :smile: , This Repositiory holds my Minor Capstone Project entrusted to me by **`Nucleus Teq Pvt Limited`**.  

The Title of my project is : **`Employee Management Portal`**  
**Details** : [**Employee Management Portal**](/Employee%20Management%20Portal%20-%20Python.pdf) 

## Index
1. [**Directory Structure**](#directory-structure)
1. [**Database**](#database)
    1. [**ER Diagram**](#er-diagram)
    1. [**SQL Code For Tables**](#sql-code-for-database-table)
    1. [**Database Connectivity**](#database-connectivity)
1. [**API**](#api)
    1. [**Main**](#main)
    1. [**Admin**](#admin)
    1. [**Manager**](#manager)
    1. [**Employee**](#employee)
1. [**Testing**](#testing)
    1. [**Test Application**](#application-test)

### **```Directory Structure```**

<details>
<summary><b>View Directory Structure</b></summary>

```
NucleusTeq-Capstone-Project
├─── .gitignore
├─── Database.sql
├─── Doubts.txt
├─── Employee Management Portal - Python.pdf
├─── LICENSE.md
├─── Notes.txt
├─── README.md
└───app
     ├───   app.log
     ├───   Dockerfile
     ├───   logging_config.py
     ├───   main.py
     ├───   requirements.txt
     ├───   __init__.py
     │
     ├───config
     │    ├───   db_connection.py
     │    └───  __init__.py
     │
     ├───models
     │   ├───   employee_model.py
     │   ├───   index_model.py
     │   ├───   project_model.py
     │   └───   __init__.py
     │
     ├───router
     │   ├───   admin_router.py
     │   ├───   emp_router.py
     │   ├───   manager_router.py
     │   └───   __init__.py
     │   
     │
     ├───schema
     │   ├───   schemas.py
     │   └───   __init__.py
     │
     ├───static
     │   ├───css
     │   │   ├───  form_style.css
     │   │   ├───  form_style_II.css
     │   │   ├───  styles.css
     │   │   ├───  table_stylesheet.css
     │   │   │
     │   │   └───admin
     │   │         ├───  assign_project.css
     │   │         ├───  home.css
     │   │         ├───  joining_request_style.css
     │   │         ├───  navigation_bar.css
     │   │         ├───  styles.css
     │   │         └───  update_skills.css
     │   │
     │   └───js
     │       ├───   joining_request.js
     │       │
     │       ├───admin
     │       │     ├───  assign_project.js
     │       │     ├───  create_project.js
     │       │     ├───  index.js
     │       │     ├───  joining_request.js
     │       │     ├───  logout.js
     │       │     ├───  manager_request.js
     │       │     ├───  remove_employee.js
     │       │     ├───  unassign_project.js
     │       │     └───  update_skills.js
     │       │
     │       ├───employee
     │       │     ├───  index.js
     │       │     ├───  logout.js
     │       │     └───  update_skills.js
     │       │
     │       └───manager
     │             ├───  filter_employee_for_project.js
     │             ├───  index.js
     │             └───  logout.js
     │
     ├─── templates
     │   ├───   index.html
     │   ├───   joining_request.html
     │   ├───   navigation_bar.html
     │   │
     │   ├───admin
     │   │    ├───   admin_navigation_bar.html
     │   │    ├───   assign_project.html
     │   │    ├───   comprehensive_info.html
     │   │    ├───   create_project.html
     │   │    ├───   home.html
     │   │    ├───   index.html
     │   │    ├───   joining_request.html
     │   │    ├───   manager_request.html
     │   │    ├───   navigation_bar.html
     │   │    ├───   remove_employee.html
     │   │    ├───   unassign_project.html
     │   │    └───   update_skill.html
     │   │
     │   ├───employee
     │   │    ├───  all_employees.html
     │   │    ├───  employee_navigation_bar.html
     │   │    ├───  employee_project.html
     │   │    ├───  home.html
     │   │    ├───  index.html
     │   │    ├───  navigation_bar.html
     │   │    └───  update_skill.html
     │   │
     │   └───manager
     │        ├───   comprehensive_info.html
     │        ├───   filter_employee_for_project.html
     │        ├───   home.html
     │        ├───   index.html
     │        ├───   manager_navigation_bar.html
     │        ├───   manager_project_info.html
     │        └───   navigation_bar.html
     │
     └───test_app
         ├─── pytest.ini
         ├─── test_admin_router.py
         ├─── test_employee_router.py
         ├─── test_main.py
         ├─── test_manager_router.py
         ├─── test_tester.py
         └─── __init__.py
    
``` 

</details>

## Database

###  **ER Diagram**

> **Diagram** : [***Open***](./images/ER%20Diagram%20of%20Database.png)

### **SQL Code For Database Table**

`Joining Request Table` holds the joining request of Manager and Employee.  
```sql
CREATE TABLE joining_request(
    id VARCHAR(30),
    name VARCHAR(30),
	password VARCHAR(100),
    emp_type VARCHAR(20),
    admin_id VARCHAR(30),
    email VARCHAR(40),
    mobile VARCHAR(11),
    gender ENUM("Male","Female","Other"),
    date_of_joining	DATE,
    status VARCHAR(10),
    PRIMARY KEY(id)
);
```
`Admin Table` Holds the details of admin.  
```sql
CREATE TABLE admin (
    admin_id VARCHAR(30) PRIMARY KEY,
    admin_name VARCHAR(40),
    password VARCHAR(100),
    email VARCHAR(50),
    mobile VARCHAR(15),
    gender ENUM('Male', 'Female', 'Other')
);
```
`Employee Table`  holds the details of employee.
```sql
CREATE TABLE employees
(
    emp_id VARCHAR(30),
    emp_name VARCHAR(30),
	password VARCHAR(100),
    admin_id VARCHAR(30),
    email VARCHAR(40),
    mobile VARCHAR(11),
    gender ENUM("Male","Female","Other"),
    skills VARCHAR(150),
    project_assigned ENUM('YES','NO') DEFAULT 'NO',
    PRIMARY KEY(emp_id),
    FOREIGN KEY(admin_id) REFERENCES admin(admin_id)
);
```
`Project Table`  holds the details of project.
```sql
CREATE TABLE project
(
    project_id VARCHAR(30),
    project_name VARCHAR(30),
    admin_id VARCHAR(30),
    start_date DATE,
    dead_line DATE,
    status VARCHAR(30),
    project_assigned ENUM("YES","NO") DEFAULT "NO",
    description MEDIUMTEXT,
    project_completed ENUM("YES","NO") DEFAULT "NO",
    PRIMARY KEY(project_id),
    FOREIGN KEY(admin_id) REFERENCES admin(admin_id)
);
```
`Project Completed Table`  holds the completed project records.
```sql
CREATE TABLE project_completed
(
    project_id VARCHAR(30),
    project_name VARCHAR(30),
    admin_id VARCHAR(30),
    admin_name VARCHAR(30),
    start_date DATE,
    dead_line DATE,
    status VARCHAR(30),
    project_completion_date DATE,
    PRIMARY KEY(project_id),
);

```
`Manager Table`  holds the manager details.
```sql
CREATE TABLE manager
(
    manager_id VARCHAR(30),
    manager_name VARCHAR(30),
    password VARCHAR(100),
    admin_id VARCHAR(30),
    email VARCHAR(40),
    mobile VARCHAR(11),
    gender ENUM("Male","Female","Other"),
    PRIMARY KEY(manager_id),
    FOREIGN KEY(admin_id) REFERENCES admin(admin_id)
);
```
`Manager project Detail Table`  holds information the manager and the project they are assign to.
```sql
CREATE TABLE manager_project_details
(
    project_id VARCHAR(30),
    manager_id VARCHAR(30),
    PRIMARY KEY(project_id,manager_id),
    FOREIGN KEY (project_id) REFERENCES project(project_id)
    ON UPDATE CASCADE ON DELETE CASCADE
);
```
`Employee project Detail Table`  holds information the employee and the project they are assign to.
```sql
CREATE TABLE employee_project_details
(
    emp_id VARCHAR(30),
    manager_id VARCHAR(30),
    project_id VARCHAR(30),
    PRIMARY KEY(emp_id),
    FOREIGN KEY(project_id , manager_id) REFERENCES manager_project_details(project_id , manager_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id) ON DELETE CASCADE
);
```
`Manager Request for Employee Table`  holds information the manager Request for employee for their project.
```sql
CREATE TABLE manager_request_for_employees
(
    emp_id VARCHAR(30),
    manager_id VARCHAR(30),
    project_id VARCHAR(30),
    admin_id VARCHAR(30),
    status VARCHAR(30),
    FOREIGN KEY (manager_id) REFERENCES manager(manager_id)
    ON DELETE CASCADE,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
    ON DELETE CASCADE
);
```
`Employee Termination Record Table`  holds the employee and manager who were removed by the admin.
```sql
CREATE TABLE employee_termination_records (
    id VARCHAR(30) PRIMARY KEY,
    name VARCHAR(30),
    emp_type VARCHAR(30),
    admin_id VARCHAR(30),
    admin_name VARCHAR(30),
    email VARCHAR(50),
    mobile VARCHAR(15),
    gender VARCHAR(20),
    date_of_joining DATE,
	departure_date DATE
);

```
`Note` : The Removed Employee, Manager and Completed project will not be part of the Employee management Protal then also I am saving it for `record management`.  

>**Database SQL Code** : [***Open***](./ER%20Diagram%20of%20Database.png)

### **Database Connectivity**

```python

import  mysql.connector as mysql_connector

def get_db():
    try:
        sql = mysql_connector.connect(host = "localhost", user = "root",passwd = "",database = "emp_management_db")
        cursor = sql.cursor()
        yield (sql,cursor)
    except Exception as e:
        print("Unable To connect the SQl Database.")

```
>**db_connection.py** : [***open***](./app/config/db_connection.py)

## API
This FastAPI application serves as a simple `employee management portal`, providing endpoints to manage employee data stored in a database. It allows you to fetch employee details by their unique ID and includes robust error handling for scenarios such as data not found and database errors.
### Main
This is the `starting point` of the FastAPI application. The Functionalities it has : 
1. Welcome Page
1. Login
1. Registration of Employee

> **main** : [***open***](./app/main.py)

### Admin
Functionalities Admin has : 

1. Admin Login
2. View all employee and project
3. Add new employee (Manager/employee)
4. Address manager request for employees
5. Assign project (manager/employee)
6. Unassign project (manager/employee)
7. Remove employee (manager/employee)
8. Update employee skill
9. create Project
10. Manager Request  for completion of project 
11. View all project
12. Logout

> **admin_router** : [***open***](./app/router/admin_router.py)
### Manager
Functionalities Manager has :
1. Manager Login Panal
2. View all employee and project
3. Filter employee (unassigned) on the basis of skill
4. Request admin for employee for project
5. View project he/she has
6. Update the status of project
7. Logout

> **manager_router** : [***open***](./app/router/manager_router.py)

### Employee
Functionalities Employee has:
1. Employee Login Panal
2. View all employee
3. View project he/she has
4. Update the skill
5. Logout

> **employee_router** : [***open***](./app/router/employee_router.py)

## Testing 

Testing ensures that your FastAPI application works as expected and helps catch issues early in the development process. I am using `pytest`, a powerful and flexible testing framework, you can write comprehensive test cases for your FastAPI endpoints.

`Note` :  Run the test command from root directory. For my project it is app.


> PS F:\Git\NucleusTeq-Capstone-project> cd app

Use `coverage module` to see how much % your test is covering the code of your program.

>PS F:\Git\NucleusTeq-Capstone-project\app> pip install coverage

### Application Test
Run below command to `Start Test`

```bash
MICROSOFT@DESKTOP-225HS7V MINGW64 /f/Git/NucleusTeq-Capstone-project/app (master)
$ coverage run -m pytest
================================== test session starts ===================================
platform win32 -- Python 3.7.4, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
rootdir: F:\Git\NucleusTeq-Capstone-project\app
plugins: anyio-3.7.1, order-1.2.1, shutil-1.7.0
collected 56 items

test_app\test_main.py ......                                                        [ 10%]
test_app\test_admin_router.py ................                                      [ 39%]
test_app\test_manager_router.py .......                                             [ 51%]
test_app\test_admin_router.py .......                                               [ 64%]
test_app\test_manager_router.py ..                                                  [ 67%]
test_app\test_admin_router.py ...                                                   [ 73%]
test_app\test_employee_router.py ........                                           [ 87%]
test_app\test_admin_router.py ....                                                  [ 94%]
test_app\test_manager_router.py .                                                   [ 96%]
test_app\test_admin_router.py ..                                                    [100%]

================================== 56 passed in 15.73s =================================== 
```
Run Below code to see the coverage of the test.
```bash 
MICROSOFT@DESKTOP-225HS7V MINGW64 /f/Git/NucleusTeq-Capstone-project/app (master)
$ coverage report --show-missing
Name                               Stmts   Miss  Cover   Missing
----------------------------------------------------------------
__init__.py                            0      0   100%
config\__init__.py                     0      0   100%
config\db_connection.py                8      0   100%
logging_config.py                      3      0   100%
main.py                               60      3    95%   75-77
models\__init__.py                     0      0   100%
models\employee_model.py              60      0   100%
models\index_model.py                 43      0   100%
models\project_model.py               34      0   100%
router\__init__.py                     0      0   100%
router\admin_router.py               674    110    84%   51, 116-118, 193-195, 296-299, 346-348, 510-512, 563-565, 655-657, 714-717, 788-791, 864-866, 912-915, 962-965, 1013-1015, 1075-1078, 1117-1120, 1164-1166, 1206-1209, 1250-1253, 1306-1308, 1345-1348, 1400-1403, 1460-1462, 1541-1543, 1604-1607, 1630-1664
router\emp_router.py                 152     25    84%   35, 38, 94-96, 172-174, 209-211, 247-250, 289-292, 334-336, 343-345
router\manager_router.py             192     30    84%   35, 38, 102-104, 122-123, 225-227, 287-289, 330-333, 382-384, 428-430, 468-471, 479-481
schema\__init__.py                     0      0   100%
schema\schemas.py                     16      0   100%
test_app\__init__.py                   0      0   100%
test_app\test_admin_router.py        195      0   100%
test_app\test_employee_router.py      40      0   100%
test_app\test_main.py                 60      0   100%
test_app\test_manager_router.py       70      0   100%
test_app\test_tester.py                6      0   100%
----------------------------------------------------------------
TOTAL                               1613    168    90%

MICROSOFT@DESKTOP-225HS7V MINGW64 /f/Git/NucleusTeq-Capstone-project/app (master)
$

```