CREATE TABLE joining_request(
    id VARCHAR(30),
    name VARCHAR(30),
	password VARCHAR(100),
    emp_type VARCHAR(20),
    admin_id VARCHAR(20),
    email VARCHAR(40),
    mobile VARCHAR(11),
    gender ENUM("Male","Female","Other"),
    status VARCHAR(10),
    PRIMARY KEY(id)
);

CREATE TABLE admin (
    admin_id VARCHAR(20) PRIMARY KEY,
    admin_name VARCHAR(40),
    password VARCHAR(100),
    email VARCHAR(50),
    mobile VARCHAR(15),
    gender ENUM('Male', 'Female', 'Other')
);

CREATE TABLE employees
(
    emp_id VARCHAR(30),
    emp_name VARCHAR(30),
	password VARCHAR(100),
    admin_id VARCHAR(20),
    email VARCHAR(40),
    mobile VARCHAR(11),
    gender ENUM("Male","Female","Other"),
    skills VARCHAR(150),
    PRIMARY KEY(emp_id),
    FOREIGN KEY(admin_id) REFERENCES admin(admin_id)
);

CREATE TABLE project
(
    project_id VARCHAR(30),
    project_name VARCHAR(30),
    admin_id VARCHAR(10),
    admin_name VARCHAR(30),
    start_date DATE,
    dead_line DATE,
    status VARCHAR(30),
    project_assigned ENUM("YES","NO"),
    project_completion_date DATE,
    description text,
    PRIMARY KEY(project_id),
    FOREIGN KEY(admin_id) REFERENCES admin(admin_id)
);

CREATE TABLE project_completed
(
    project_id VARCHAR(30),
    project_name VARCHAR(30),
    admin_id VARCHAR(10),
    admin_name VARCHAR(30),
    start_date DATE,
    dead_line DATE,
    status VARCHAR(30),
    project_completion_date DATE,
    PRIMARY KEY(project_id),
);


CREATE TABLE manager
(
    manager_id VARCHAR(30),
    manager_name VARCHAR(30),
    password VARCHAR(100),
    admin_id VARCHAR(20),
    admin_name VARCHAR(30),
    email VARCHAR(40),
    mobile VARCHAR(11),
    gender ENUM("Male","Female","Other"),
    PRIMARY KEY(manager_id),
    FOREIGN KEY(admin_id) REFERENCES admin(admin_id)
);

CREATE TABLE manager_project_details
(
    project_id VARCHAR(30),
    manager_id VARCHAR(30),
    PRIMARY KEY(project_id,manager_id),
    FOREIGN KEY (project_id) REFERENCES project(project_id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

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

CREATE TABLE employee_termination_records (
    id VARCHAR(20) PRIMARY KEY,
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


INSERT INTO admin (admin_id, admin_name, password, email, mobile, gender)
VALUES 
    ("ADM001", 'Admin1', 'password1', 'admin1@example.com', '1234567890', 'Male'),
    ("ADM002", 'Admin2', 'password2', 'admin2@example.com', '9876543210', 'Female'),
    ("ADM003", 'Admin3', 'password3', 'admin3@example.com', '5555555555', 'Other');
     
-- Managers working under Admin1
INSERT INTO manager (manager_id, manager_name, password, admin_id, admin_name, email, mobile, gender)
VALUES 
    ('MGR001', 'Manager1', 'password1', 'ADM001', 'Admin1', 'manager1@example.com', '12345678901', 'Male'),
    ('MGR002', 'Manager2', 'password2', 'ADM001', 'Admin1', 'manager2@example.com', '23456789012', 'Female'),
    ('MGR003', 'Manager3', 'password3', 'ADM001', 'Admin1', 'manager3@example.com', '34567890123', 'Other');

-- Managers working under Admin2
INSERT INTO manager (manager_id, manager_name, password, admin_id, admin_name, email, mobile, gender)
VALUES 
    ('MGR004', 'Manager4', 'password4', 'ADM002', 'Admin2', 'manager4@example.com', '45678901234', 'Male'),
    ('MGR005', 'Manager5', 'password5', 'ADM002', 'Admin2', 'manager5@example.com', '56789012345', 'Female'),
    ('MGR006', 'Manager6', 'password6', 'ADM002', 'Admin2', 'manager6@example.com', '67890123456', 'Other');

-- Managers working under Admin3
INSERT INTO manager (manager_id, manager_name, password, admin_id, admin_name, email, mobile, gender)
VALUES 
    ('MGR007', 'Manager7', 'password7', 'ADM003', 'Admin3', 'manager7@example.com', '78901234567', 'Male'),
    ('MGR008', 'Manager8', 'password8', 'ADM003', 'Admin3', 'manager8@example.com', '89012345678', 'Female'),
    ('MGR009', 'Manager9', 'password9', 'ADM003', 'Admin3', 'manager9@example.com', '90123456789', 'Other');

-- Employees working under Admin1
INSERT INTO employees (emp_id, emp_name, password, admin_id, admin_name, email, mobile, gender, skills)
VALUES 
    ('EMP001', 'Employee1', 'password1', 'ADM001', 'Admin1', 'employee1@example.com', '12345678901', 'Male', 'Skill1, Skill2, Skill3'),
    ('EMP002', 'Employee2', 'password2', 'ADM001', 'Admin1', 'employee2@example.com', '23456789012', 'Female', 'Skill4, Skill5, Skill6'),
    ('EMP003', 'Employee3', 'password3', 'ADM001', 'Admin1', 'employee3@example.com', '34567890123', 'Other', 'Skill7, Skill8, Skill9');

-- Employees working under Admin2
INSERT INTO employees (emp_id, emp_name, password, admin_id, admin_name, email, mobile, gender, skills)
VALUES 
    ('EMP004', 'Employee4', 'password4', 'ADM002', 'Admin2', 'employee4@example.com', '45678901234', 'Male', 'Skill10, Skill11, Skill12'),
    ('EMP005', 'Employee5', 'password5', 'ADM002', 'Admin2', 'employee5@example.com', '56789012345', 'Female', 'Skill13, Skill14, Skill15'),
    ('EMP006', 'Employee6', 'password6', 'ADM002', 'Admin2', 'employee6@example.com', '67890123456', 'Other', 'Skill16, Skill17, Skill18');

-- Employees working under Admin3
INSERT INTO employees (emp_id, emp_name, password, admin_id, admin_name, email, mobile, gender, skills)
VALUES 
    ('EMP007', 'Employee7', 'password7', 'ADM003', 'Admin3', 'employee7@example.com', '78901234567', 'Male', 'Skill19, Skill20, Skill21'),
    ('EMP008', 'Employee8', 'password8', 'ADM003', 'Admin3', 'employee8@example.com', '89012345678', 'Female', 'Skill22, Skill23, Skill24'),
    ('EMP009', 'Employee9', 'password9', 'ADM003', 'Admin3', 'employee9@example.com', '90123456789', 'Other', 'Skill25, Skill26, Skill27');

-- Projects for Admin1
INSERT INTO project (project_id, project_name, admin_id, admin_name, start_date, dead_line, status, project_assigned, project_completion_date)
VALUES 
    ('PROJ001', 'Project1', 'ADM001', 'Admin1', '2024-01-01', '2024-06-30', 'In Progress', 'YES', NULL),
    ('PROJ002', 'Project2', 'ADM001', 'Admin1', '2024-02-01', '2024-07-31', 'Pending', 'NO', NULL),
    ('PROJ003', 'Project3', 'ADM001', 'Admin1', '2024-03-01', '2024-08-31', 'Completed', 'YES', '2024-09-15');

-- Projects for Admin2
INSERT INTO project (project_id, project_name, admin_id, admin_name, start_date, dead_line, status, project_assigned, project_completion_date)
VALUES 
    ('PROJ004', 'Project4', 'ADM002', 'Admin2', '2024-04-01', '2024-09-30', 'In Progress', 'YES', NULL),
    ('PROJ005', 'Project5', 'ADM002', 'Admin2', '2024-05-01', '2024-10-31', 'Pending', 'NO', NULL),
    ('PROJ006', 'Project6', 'ADM002', 'Admin2', '2024-06-01', '2024-11-30', 'Completed', 'YES', '2024-12-15');

-- Projects for Admin3
INSERT INTO project (project_id, project_name, admin_id, admin_name, start_date, dead_line, status, project_assigned, project_completion_date)
VALUES 
    ('PROJ007', 'Project7', 'ADM003', 'Admin3', '2024-07-01', '2024-12-31', 'In Progress', 'YES', NULL),
    ('PROJ008', 'Project8', 'ADM003', 'Admin3', '2024-08-01', '2025-01-31', 'Pending', 'NO', NULL),
    ('PROJ009', 'Project9', 'ADM003', 'Admin3', '2024-09-01', '2025-02-28', 'Completed', 'YES', '2025-03-15');

-- MANAGER_PROJECT_DETAILS
INSERT INTO manager_project_details (manager_id, project_id)
VALUES
    ('MGR001', 'PROJ001'),  -- Manager1 in Project1
    ('MGR001', 'PROJ002'),  -- Manager1 in Project2
    ('MGR002', 'PROJ003'),  -- Manager2 in Project3
    ('MGR002', 'PROJ004'),  -- Manager2 in Project4
    ('MGR003', 'PROJ005'),  -- Manager3 in Project5
    ('MGR003', 'PROJ006'),  -- Manager3 in Project6
    ('MGR004', 'PROJ007'),  -- Manager4 in Project7
    ('MGR004', 'PROJ008'),  -- Manager4 in Project8
    ('MGR005', 'PROJ009'); 


-- Data for employee_project_details
INSERT INTO employee_project_details (emp_id, manager_id, project_id)
VALUES
    ('EMP001', 'MGR001', 'PROJ001'),  -- Employee1 in Project1 managed by Manager1
    ('EMP002', 'MGR002', 'PROJ003'),  -- Employee2 in Project2 managed by Manager2
    ('EMP003', 'MGR003', 'PROJ005'),  -- Employee3 in Project3 managed by Manager3
    ('EMP004', 'MGR004', 'PROJ007'),  -- Employee4 in Project4 managed by Manager4
    ('EMP005', 'MGR001', 'PROJ001'),  -- Employee5 in Project5 managed by Manager1
    ('EMP006', 'MGR002', 'PROJ003'),  -- Employee6 in Project6 managed by Manager2
    ('EMP007', 'MGR003', 'PROJ006'),  -- Employee7 in Project7 managed by Manager3
    ('EMP008', 'MGR004', 'PROJ007'),  -- Employee8 in Project8 managed by Manager4
    ('EMP009', 'MGR001', 'PROJ002');

-- manager_request_for_employees
INSERT INTO manager_request_for_employees (emp_id, manager_id, project_id, admin_id, status)
VALUES
    ('EMP001', 'MGR001', 'PROJ001', 'ADM001', 'Pending'),  -- Manager1 requesting Employee1 for Project1 to Admin1
    ('EMP002', 'MGR002', 'PROJ002', 'ADM001', 'Approved'),  -- Manager2 requesting Employee2 for Project2 to Admin1
    ('EMP003', 'MGR003', 'PROJ003', 'ADM001', 'Pending'),  -- Manager3 requesting Employee3 for Project3 to Admin1
    ('EMP004', 'MGR004', 'PROJ004', 'ADM002', 'Approved'),  -- Manager4 requesting Employee4 for Project4 to Admin2
    ('EMP005', 'MGR001', 'PROJ005', 'ADM002', 'Pending'),  -- Manager1 requesting Employee5 for Project5 to Admin2
    ('EMP006', 'MGR002', 'PROJ006', 'ADM002', 'Approved'),  -- Manager2 requesting Employee6 for Project6 to Admin2
    ('EMP007', 'MGR003', 'PROJ007', 'ADM003', 'Pending'),  -- Manager3 requesting Employee7 for Project7 to Admin3
    ('EMP008', 'MGR004', 'PROJ008', 'ADM003', 'Approved'),  -- Manager4 requesting Employee8 for Project8 to Admin3
    ('EMP009', 'MGR001', 'PROJ009', 'ADM003', 'Pending'); 

-- To see Admin project manager and employees in comprehensive way

SELECT a.admin_id, a.admin_name , m.manager_id , m.manager_name , mpd.project_id,epd.emp_id
FROM admin AS a
INNER JOIN manager AS m 
ON a.admin_id = m.admin_id
INNER JOIN manager_project_details AS mpd
ON m.manager_id = mpd.manager_id
INNER JOIN employee_project_details AS epd
ON epd.manager_id = m.manager_id AND epd.project_id = mpd.project_id
;


-- TEST1: Delete project from project table and the related project in manager_project_deatils and emp_project_details will also be deleted.
START TRANSACTION;

DELETE FROM project
WHERE project_id = "PROJ002";

SELECT * FROM project;
select * from manager_project_details;
select * from employee_project_details;

ROLLBACK;
-- The Test Passed
-- Test2: Update the manager_id in manager_project_details it must also update in employee_project_details.

START TRANSACTION;

UPDATE manager_project_details
SET manager_id = "MGR008";

SELECT * FROM manager;
select * from manager_project_details;
select * from employee_project_details;

ROLLBACK;
-- Test Passed

-- Test3: Delete manager and it must not affect the manager_project_details.
START TRANSACTION;

DELETE FROM manager
WHERE manager_id = "MGR001";

SELECT * FROM manager;
select * from manager_project_details;
select * from employee_project_details;

ROLLBACK;
-- Test Passed

-- Test4: Remove a employee its record in employee_project_record must delete.

START TRANSACTION;

DELETE FROM employees
WHERE emp_id = "EMP001";

SELECT * FROM employees;
select * from manager_project_details;
select * from employee_project_details;

ROLLBACK;
-- Test Passed

-- Test 5: if employee is removed the corrospondin records of the employee in manager_request_for_employees will also be removed.

START TRANSACTION;

DELETE FROM employees
WHERE emp_id = "EMP001";

SELECT * FROM employees;
select * from manager_request_for_employees;
select * from employee_project_details;

ROLLBACK;
-- Test Passed.

--Test 6: if manager is removed the corrosponding records of the manger in manager_request_for_employees will also be removed.

START TRANSACTION;

DELETE FROM manager
WHERE manager_id = "MGR001";

SELECT * FROM employees;
select * from manager_request_for_employees;
select * from employee_project_details;

ROLLBACK;

-- Test Passed.

-- Data for your_table_name (including managers and employees)
INSERT INTO joining_request (id, name, password, emp_type, admin_id, admin_name, email, mobile, gender, date_of_joining, status)
VALUES
    ('EMP010', 'John', 'password1', 'Employee', 'ADM001', 'Admin1', 'john@example.com', '1234567890', 'Male', '2023-01-01', 'Active'),
    ('MGR011', 'Alice', 'password2', 'Employee', 'ADM001', 'Admin1', 'alice@example.com', '2345678901', 'Female', '2023-02-01', 'Active'),
    ('MGR010', 'Bob', 'password3', 'Manager', 'ADM002', 'Admin2', 'bob@example.com', '3456789012', 'Male', '2023-03-01', 'Inactive'),
    ('EMP011', 'Eve', 'password4', 'Manager', 'ADM002', 'Admin2', 'eve@example.com', '4567890123', 'Female', '2023-04-01', 'Active'),
    ('EMP012', 'Charlie', 'password5', 'Employee', 'ADM003', 'Admin3', 'charlie@example.com', '5678901234', 'Male', '2023-05-01', 'Active'),
    ('EMP013', 'Diana', 'password6', 'Employee', 'ADM003', 'Admin3', 'diana@example.com', '6789012345', 'Female', '2023-06-01', 'Active');
