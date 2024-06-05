This section has all the `SQL Query` that I have used in my project.

## Index
1. [**Main**](#main)
1. [**Admin**](#admin)
1. [**Manager**](#manager)
1. [**employee**](#employee)

## Main
#### @app.get("/registration_form")

`Query to fetch all the admin`

```sql
SELECT DISTINCT admin_id, admin_name FROM admin;
```
#### @app.post("/registration_form_submission", response_class=JSONResponse)  

`Query to Insert value into Joining Request Table`
```sql
INSERT INTO joining_request (id, name, password, emp_type, admin_id, email, mobile, gender, date_of_joining, status)
VALUES 
('{joining_request.id}',
'{joining_request.name}', 
'{joining_request.password}',   
'{joining_request.emp_type}',
'{joining_request.admin_id}',
'{joining_request.email}',
'{joining_request.mobile}',
'{joining_request.gender}',
'{joining_request.date_of_joining}',
'Pending')

```
## Admin
#### @admin_router.post(r"/admin_login_data", response_class=HTMLResponse)

```sql
SELECT COUNT(admin_id), admin_id, password 
FROM admin
WHERE admin_id = '{login_details.username}' AND password = '{login_details.password}';
```

#### @admin_router.get(r"/joining_request", response_class=HTMLResponse)

```sql
SELECT jr.id, jr.name, jr.emp_type, jr.admin_id, jr.email, jr.mobile, jr.gender, jr.date_of_joining, a.admin_name
FROM joining_request AS jr, admin AS a
WHERE jr.status = 'Pending' AND jr.admin_id = '{admin_id}' AND a.admin_id = '{admin_id}';

```

#### @admin_router.post(r"/accept_joining_request", response_class=JSONResponse)

```sql
-- For Employee
INSERT INTO employees (emp_id, emp_name, password, admin_id, email, mobile, gender, skills)
SELECT id, name, password, admin_id, email, mobile, gender, 'None'
FROM joining_request
WHERE id = '{joining_request.id}';

-- For Manager
INSERT INTO manager (manager_id, manager_name, password, admin_id, email, mobile, gender)
SELECT id, name, password, admin_id, email, mobile, gender
FROM joining_request
WHERE id = '{joining_request.id}';

-- Update Status
UPDATE joining_request
SET status = 'Approved'
WHERE id = '{joining_request.id}';
```

#### @admin_router.post(r"/reject_joining_request", response_class=JSONResponse)

```sql
UPDATE joining_request
SET status = 'Rejected'
WHERE id = '{joining_request.id}';
```

#### @admin_router.get(r"/create_project_form", response_class=HTMLResponse)

```sql
SELECT manager_id, manager_name
FROM manager
WHERE admin_id = '{admin_id}';
```

#### @admin_router.post(r"/create_project_form_processing", response_class=JSONResponse)
```sql
-- Insert into manager_project_details
INSERT INTO manager_project_details (manager_id, project_id)
VALUES ('{project_details.assign_to}','{project_details.project_id}');

-- Create project
INSERT INTO project (project_id, project_name, admin_id, start_date, dead_line, status, project_assigned, description)
VALUES (
    '{project_details.project_id}',
    '{project_details.project_name}', 
    '{project_details.admin_id}',
    '{start_date}',
    '{project_details.dead_line}',
    '{status_value}',
    '{project_assigned}',
    '{project_details.description}'
);

```
#### @admin_router.get(r"/admin_view_all", response_class=HTMLResponse)

```sql 
-- Employee data
SELECT e.emp_id, e.emp_name, e.gender, e.email, e.admin_id, a.admin_name, m.manager_id, m.manager_name, p.project_id, p.project_name
FROM employees AS e
LEFT JOIN employee_project_details AS epd ON e.emp_id = epd.emp_id
LEFT JOIN project AS p ON p.project_id = epd.project_id
LEFT JOIN manager AS m ON m.manager_id = epd.manager_id
LEFT JOIN admin AS a ON e.admin_id = a.admin_id
ORDER BY e.admin_id ASC;

-- Manager Data
SELECT m.manager_id, m.manager_name, m.gender, m.email, m.admin_id, a.admin_name, GROUP_CONCAT(mpd.project_id), GROUP_CONCAT(p.project_name)
FROM manager AS m
LEFT JOIN manager_project_details AS mpd ON m.manager_id = mpd.manager_id
LEFT JOIN project AS p ON p.project_id = mpd.project_id
LEFT JOIN admin AS a ON m.admin_id = a.admin_id
GROUP BY m.manager_id
ORDER BY m.admin_id ASC;

-- Project data
SELECT p.project_id, p.project_name, p.admin_id, a.admin_name, p.start_date, p.dead_line, mpd.manager_id, m.manager_name, p.status
FROM project AS p
LEFT JOIN manager_project_details AS mpd ON mpd.project_id = p.project_id
LEFT JOIN manager AS m ON mpd.manager_id = m.manager_id
LEFT JOIN admin AS a ON p.admin_id = a.admin_id
ORDER BY p.admin_id ASC;

```
#### @admin_router.get(r"/admin_view_all_project", response_class=HTMLResponse)

```sql
SELECT p.project_id, p.project_name, p.admin_id, a.admin_name, p.start_date, p.dead_line, mpd.manager_id, m.manager_name, p.status, p.description
FROM project AS p
LEFT JOIN manager_project_details AS mpd ON mpd.project_id = p.project_id
LEFT JOIN manager AS m ON mpd.manager_id = m.manager_id
LEFT JOIN admin AS a ON p.admin_id = a.admin_id
WHERE p.admin_id = '{admin_id}'
ORDER BY p.admin_id ASC;
```

#### @admin_router.get(r"/assign_project", response_class=HTMLResponse)

```sql
-- For Employee details
SELECT e.emp_id, e.emp_name, e.gender, e.mobile, e.email, e.skills
FROM employees AS e
WHERE project_assigned IN ('NO','') AND admin_id = '{admin_id}'; 

-- Project that can be assigned to employees
SELECT p.project_id, p.project_name 
FROM project AS p
INNER JOIN manager_project_details AS mpd
ON mpd.project_id = p.project_id
WHERE p.project_assigned = "YES" AND admin_id = '{admin_id}';

-- For getting managers detail
SELECT m.manager_id , m.manager_name, m.gender, m.mobile, m.email, 
GROUP_CONCAT(DISTINCT mpd.project_id ORDER BY mpd.project_id ASC SEPARATOR ', ') AS project_they_have,
GROUP_CONCAT(DISTINCT p.project_name ORDER BY p.project_id ASC SEPARATOR ', ') AS project_names
FROM manager AS m
LEFT JOIN manager_project_details AS mpd
ON m.manager_id = mpd.manager_id
LEFT JOIN project AS p
ON p.project_id = mpd.project_id
WHERE m.admin_id = '{admin_id}'
GROUP BY m.manager_id;

-- Project that can be assigned to Manager
SELECT project_id, project_name 
FROM project 
WHERE project_assigned = 'NO' ;""" 
```
#### @admin_router.post(r"/assign_employee_a_project",response_class=JSONResponse)


```sql 
-- Insert data to Employee projet table
INSERT INTO employee_project_details (emp_id,manager_id,project_id)
    WITH employee_project_data AS (
        SELECT '{employee_data.emp_id}' AS emp_id, mpd.manager_id AS manager_id ,'{employee_data.project_id}' AS project_id 
        FROM manager_project_details AS mpd
        WHERE mpd.project_id = '{employee_data.project_id}'
    )
    SELECT emp_id , manager_id , project_id FROM employee_project_data ;

-- Update Project assigned column of employee
UPDATE employees
SET project_assigned = "YES"
WHERE emp_id = '{employee_data.emp_id}' ;
```

#### @admin_router.post(r"/assign_manager_a_project",response_class=JSONResponse)

```sql 
-- To see project record exist
SELECT COUNT(project_id) 
FROM manager_project_details
WHERE project_id = '{manager_data.project_id}';

-- Update Manager Project Table records
UPDATE manager_project_details 
SET manager_id = '{manager_data.manager_id}'
WHERE project_id = '{manager_data.project_id}';

-- Insert Value in Manager Project details
INSERT INTO manager_project_details (manager_id,project_id)
VALUES('{manager_data.manager_id}','{manager_data.project_id}');

-- Update project project_Assigned Column
UPDATE project
SET project_assigned = 'YES', status = 'Started'
WHERE project_id = '{manager_data.project_id}' ;
```
#### @admin_router.get(r"/unassign_project",response_class=HTMLResponse)

```sql
-- For Employee who are assigned to project
SELECT e.emp_id,e.emp_name, e.gender , e.mobile , e.email,
p.project_id , p.project_name, m.manager_id , m.manager_name
FROM employees AS e
INNER JOIN employee_project_details AS epd
ON e.emp_id = epd.emp_id 
INNER JOIN project AS p
ON p.project_id = epd.project_id
INNER JOIN manager  AS m
ON m.manager_id = epd.manager_id
WHERE e.admin_id = '{admin_id}'
;

-- Manager Who are assigned to Project
SELECT m.manager_id , m.manager_name , m.gender , m.mobile , m.email,
GROUP_CONCAT(DISTINCT p.project_id ORDER BY p.project_id ASC SEPARATOR ', ') AS project_id,
GROUP_CONCAT(DISTINCT p.project_name ORDER BY p.project_id ASC SEPARATOR ', ') AS project_name
FROM manager_project_details AS mpd
INNER JOIN manager AS m
ON m.manager_id = mpd.manager_id
INNER JOIN project AS p
ON p.project_id = mpd.project_id
WHERE m.admin_id = '{admin_id}' 
GROUP BY m.manager_id ;

```
#### @admin_router.put(r"/unassign_employee_from_project",response_class=JSONResponse)
```sql
-- Delete the employee records
DELETE FROM employee_project_details
WHERE emp_id = '{employee_data.emp_id}' ;

-- Update the project assigned status
UPDATE employees
SET project_assigned = 'NO'
WHERE emp_id = '{employee_data.emp_id}' ;
```
#### @admin_router.put(r"/unassign_manager_from_project",response_class=JSONResponse)

```sql
-- Update Manager Project Details
UPDATE manager_project_details
SET manager_id = 'Unassigned'
WHERE manager_id = '{manager_data.manager_id}' AND project_id = '{manager_data.project_id}' ;

-- Update the project Table
UPDATE project
SET project_assigned = 'NO',
status = 'On Hold'
WHERE project_id = '{manager_data.project_id}'; 
    
```
#### @admin_router.get(r"/manager_request",response_class=HTMLResponse)

```sql
-- For fetching the manager request
SELECT m.manager_name, m.manager_id, p.project_name , p.project_id , e.emp_name , e.emp_id
FROM manager_request_for_employees AS mrfe
INNER JOIN manager AS m
ON mrfe.manager_id = m.manager_id
INNER JOIN project AS p
ON mrfe.project_id = p.project_id
INNER JOIN employees AS e
ON mrfe.emp_id = e.emp_id
WHERE mrfe.status = "Pending" AND mrfe.admin_id = '{admin_id}'
GROUP BY m.manager_id, p.project_id,e.emp_id;
```
#### @admin_router.post(r"/accept_manager_request",response_class=JSONResponse)

```sql
-- Insert value to Manager Project detail
INSERT INTO employee_project_details (emp_id,project_id,manager_id)
VALUES ('{manager_request_for_employees.emp_id}', '{manager_request_for_employees.project_id}', '{manager_request_for_employees.manager_id}')

-- Update status
UPDATE manager_request_for_employees
SET status = 'Approved'
WHERE emp_id = '{manager_request_for_employees.emp_id}' AND project_id = '{manager_request_for_employees.project_id}' AND manager_id = '{manager_request_for_employees.manager_id}';

-- Ipdate the empoyee project assigned status
UPDATE employees
SET project_assigned = 'YES'
WHERE emp_id = '{manager_request_for_employees.emp_id}';"""
logger.debug(f"[Query 3]: SQL Query to Update the project_assigned column of employees : {sql_query_to_update_employee_record} ") 
```
#### @admin_router.put(r"/reject_manager_request",response_class=JSONResponse)
```sql
UPDATE manager_request_for_employees
SET status = 'Rejected'
WHERE emp_id = '{manager_request_for_employees.emp_id}' AND project_id = '{manager_request_for_employees.project_id}' AND manager_id = '{manager_request_for_employees.manager_id}';

```
#### @admin_router.get(r"/update_employee_skill",response_class=HTMLResponse)
```sql
SELECT e.emp_id, e.emp_name, e.gender, e.mobile, e.email, e.skills
FROM employees AS e
WHERE admin_id = '{admin_id}';
```
#### @admin_router.put(r"/add_employee_skill",response_class=JSONResponse)
```sql
UPDATE employees
SET skills = CONCAT(skills,' {employee_data.skills}')
WHERE emp_id = '{employee_data.emp_id}';
```
#### @admin_router.put(r"/replace_employee_skill",response_class=JSONResponse)
```sql
UPDATE employees
SET skills =  '{employee_data.skills}'
WHERE emp_id = '{employee_data.emp_id}';
```
#### admin_router.get(r"/manager_request_to_complete_project",response_class=HTMLResponse)
```sql
SELECT p.project_id , p.project_name ,p.admin_id, a.admin_name, p.start_date, p.dead_line, mpd.manager_id, m.manager_name , p.status
FROM project AS p
LEFT JOIN manager_project_details AS mpd
ON mpd.project_id = p.project_id
LEFT JOIN manager AS m
ON mpd.manager_id = m.manager_id
LEFT JOIN admin as a
ON p.admin_id = a.admin_id
WHERE p.status = 'completed'
ORDER BY p.admin_id ASC;
```

#### @admin_router.put("/reject_completion_of_project")
```sql
UPDATE project
SET status = 'Review'
WHERE project_id = '{project_id}'
```
#### @admin_router.delete("/approve_completion_of_project")

```sql
-- Update employee record
UPDATE employees
SET project_assigned = 'NO'
WHERE emp_id IN (SELECT emp_id FROM employee_project_details WHERE project_id = '{project_id}');

-- Save Record into Project completed Table
INSERT INTO project_completed(project_id,project_name, admin_id,admin_name, start_date, dead_line, status, description , project_completion_date)
SELECT p.project_id , p.project_name, p.admin_id , a.admin_name , p.start_date, p.dead_line, p.status, p.description , CURDATE()
FROM project AS p , admin AS a
WHERE project_id = '{project_id}' AND a.admin_id = p.admin_id;

-- delete the project
DELETE FROM project WHERE project_id = '{project_id}';

```
#### @admin_router.get(r"/remove_workers",response_class=HTMLResponse)

```sql
-- fetch the manager details
SELECT manager_name, manager_id, email,mobile , gender
FROM manager
WHERE admin_id = '{admin_id}'

-- fetch the employee details
SELECT emp_name, emp_id, email,mobile , gender
FROM employees
WHERE admin_id = '{admin_id}'
```
#### @admin_router.delete("/remove_manager",response_class=JSONResponse)

```sql 
-- Save  the manager data in employee ternination record
INSERT INTO employee_termination_records (id,name,emp_type,admin_id,admin_name,email,mobile,gender,date_of_joining,departure_date)
WITH manager_data AS(
    SELECT m.manager_id , m.manager_name ,'Manager', m.admin_id , a.admin_name , m.email , m.mobile , m.gender , jr.date_of_joining, CURDATE()
    FROM manager AS m
    INNER JOIN admin AS a
    ON a.admin_id = m.admin_id
    INNER JOIN joining_request AS jr
    ON m.manager_id = jr.id AND m.admin_id = jr.admin_id
    WHERE m.manager_id = '{manager_id}'
)
SELECT * FROM manager_data;

-- Delete Manager 
DELETE FROM manager
WHERE manager_id = '{manager_id}' ;

-- Update manager project details
UPDATE manager_project_details
set manager_id = 'Terminated'
WHERE manager_id = '{manager_id}';

-- Update project table
UPDATE project
SET project_assigned = 'NO'
WHERE project_id in (
    SELECT project_id FROM manager_project_details WHERE manager_id = '{manager_id}'
    );
    
```

#### @admin_router.delete("/remove_employee", response_class=JSONResponse)

```sql
--  Delete the employee record
DELETE FROM employees
WHERE emp_id = '{emp_id}' ;

-- save the employee record
INSERT INTO employee_termination_records (id,name,emp_type,admin_id,admin_name,email,mobile,gender,date_of_joining,departure_date)
WITH manager_data AS(
    SELECT e.emp_id , e.emp_name ,'Employee', e.admin_id , a.admin_name , e.email , e.mobile , e.gender , jr.date_of_joining, CURDATE()
    FROM employees AS e
    INNER JOIN admin AS a
    ON a.admin_id = e.admin_id
    INNER JOIN joining_request AS jr
    ON e.emp_id = jr.id AND e.admin_id = jr.admin_id
    WHERE e.emp_id = '{emp_id}'
)
SELECT * FROM manager_data;
``` 
## Manager

#### @manager_router.post(r"/manager_login_data", response_class = HTMLResponse)

```sql
SELECT COUNT(manager_id) ,manager_id, password 
FROM manager
WHERE manager_id = '{login_details.username}' AND password = '{login_details.password}' ;
```

#### @manager_router.get(r"/comprehensive_info")
```sql 
SELECT e.emp_id, e.emp_name, e.gender, e.email,e.admin_id,a.admin_name ,m.manager_id , m.manager_name , p.project_id , p.project_name
FROM employees AS e
LEFT JOIN employee_project_details AS epd
ON e.emp_id = epd.emp_id
LEFT JOIN project AS p
ON p.project_id = epd.project_id
LEFT JOIN manager AS m
ON m.manager_id = epd.manager_id 
LEFT JOIN admin AS a
ON a.admin_id = e.admin_id
ORDER BY a.admin_id ASC;

SELECT m.manager_id, m.manager_name, m.gender, m.email,m.admin_id,a.admin_name , GROUP_CONCAT(mpd.project_id) , GROUP_CONCAT(p.project_name)
FROM manager AS m
LEFT JOIN manager_project_details AS mpd
ON m.manager_id = mpd.manager_id
LEFT JOIN project AS p
ON p.project_id = mpd.project_id
LEFT JOIN admin AS a
ON a.admin_id = m.admin_id
GROUP BY m.manager_id ;

SELECT p.project_id , p.project_name , a.admin_id , a.admin_name,p.start_date, p.dead_line, mpd.manager_id, m.manager_name 
FROM project AS p
LEFT JOIN manager_project_details AS mpd
ON mpd.project_id = p.project_id
LEFT JOIN manager AS m
ON mpd.manager_id = m.manager_id
LEFT JOIN admin AS a
ON a.admin_id = p.admin_id
;
```

#### @manager_router.get(r"/filtered_employee")
```sql 
SELECT e.emp_id , e.emp_name , e.gender , e.mobile , e.email , e.skills
FROM employees AS e,manager AS m
WHERE m.manager_id = '{manager_id}' AND e.admin_id = m.admin_id AND e.project_assigned = 'NO' AND e.skills REGEXP '{skill}';


SELECT mpd.project_id , p.project_name
FROM manager_project_details AS mpd
INNER JOIN project AS p
ON p.project_id = mpd.project_id
WHERE mpd.manager_id = '{manager_id}';
```

#### @manager_router.post(r"/request_for_employee", response_class=JSONResponse)

```sql
INSERT INTO manager_request_for_employees (emp_id, manager_id, project_id,admin_id,status)
WITH request_details AS(
SELECT '{employee_data.emp_id}' , '{employee_data.manager_id}' , '{employee_data.project_id}' , admin_id , 'Pending'
FROM manager 
WHERE manager_id = '{employee_data.manager_id}'
)
SELECT * FROM request_details ;
```
#### @manager_router.get(r"/projects_manager_have")

```sql
SELECT p.project_id , p.project_name , p.start_date , p.dead_line, p.status , p.description
FROM  project AS p
INNER JOIN manager_project_details AS mpd
ON mpd.project_id = p.project_id
WHERE mpd.manager_id = '{manager_id}';

```

#### @manager_router.get("/update_project_status")

```sql 
SELECT p.project_id , p.project_name , p.start_date , p.dead_line, p.status , p.description
FROM  project AS p
INNER JOIN manager_project_details AS mpd
ON mpd.project_id = p.project_id
WHERE mpd.manager_id = '{manager_id}';
```

#### @manager_router.put("/update_project_status")

```sql
UPDATE project 
SET status = '{project_info.status}'
WHERE project_id = '{project_info.project_id}'
```


## Employee

#### @emp_router.post(r"/employee_login_data", response_class = HTMLResponse)

```sql
SELECT COUNT(emp_id) ,emp_id, password 
FROM employees
WHERE emp_id = '{login_details.username}' AND password = '{login_details.password}' ;

```
#### @emp_router.get(r"/employee_for_project")

```sql
SELECT e.emp_id, e.emp_name, e.gender, e.email,e.admin_id,a.admin_name ,m.manager_id , m.manager_name , p.project_id , p.project_name
FROM employees AS e
LEFT JOIN employee_project_details AS epd
ON e.emp_id = epd.emp_id
LEFT JOIN project AS p
ON p.project_id = epd.project_id
LEFT JOIN manager AS m
ON m.manager_id = epd.manager_id
LEFT JOIN admin AS a
ON a.admin_id = e.admin_id;
```

#### @emp_router.get(r"/update_skills_as_employee")

```sql
SELECT emp_id , emp_name , gender , mobile , email , skills
FROM employees WHERE emp_id = '{emp_id}' ;
```

#### @emp_router.put(r"/add_skill",response_class=JSONResponse)

```sql
UPDATE employees
SET skills = CONCAT(skills,' {employee_data.skills}')
WHERE emp_id = '{employee_data.emp_id}';
```

#### @emp_router.put(r"/replace_skill",response_class=JSONResponse)

```sql 
UPDATE employees
SET skills =  '{employee_data.skills}'
WHERE emp_id = '{employee_data.emp_id}';
```

#### @emp_router.get(r"/employee_project_details")

```sql 
SELECT p.project_id, p.project_name , p.start_date, p.dead_line, m.manager_id, m.manager_name, p.description
FROM employee_project_details AS epd
INNER JOIN manager AS m
ON m.manager_id = epd.manager_id
INNER JOIN project AS p
ON p.project_id = epd.project_id
WHERE emp_id = '{emp_id}';
```