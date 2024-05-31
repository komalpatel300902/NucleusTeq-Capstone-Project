## Introduction

Welcome Everyone :smile: , This Repositiory holds my Minor Capstone Project entrusted to me by **`Nucleus Teq Pvt Limited`**.  

The Title of my project is : **`Employee Management Portal`**  
**Details** : [Employee Management Portal](/Employee%20Management%20Portal%20-%20Python.pdf) 

**```Directory Structure```**

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