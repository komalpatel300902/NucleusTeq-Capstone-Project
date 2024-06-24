This section has the route architectur of the project.

## Index
1. [**Main**](#main)
1. [**Admin**](#admin)
1. [**Manager**](#manager)
1. [**employee**](#employee)


## Main 

```bash
main.py
│
├─── [GET] /
└─── [GET] /registration_form
                └─── [POST] /registration_form
```
## Admin
```bash
admin_router.py
│
├─── [GET] /admin_login
│                 └─── [POST] /admin_login
│
├─── [GET] /admin_home
│
├─── [GET] /joining_request
│                 ├─── [POST] /accept_joining_request
│                 └─── [POST] /reject_joining_request
│
├─── [GET] /create_project_form
│                 └─── [POST] /create_project_form
├─── [GET] /admin_view_all
│
├─── [GET] /admin_view_all_project
│
├─── [GET] /assign_project
│                 ├─── [POST] /assign_employee_a_project
│                 └─── [POST] /assign_manager_a_project
│
├─── [GET] /unassign_project
│                 ├─── [PUT] /unassign_employee_from_project
│                 └─── [PUT] /unassign_manager_from_project
│
├─── [GET] /manager_request
│                 ├─── [POST] /accept_manager_request
│                 └─── [PUT] /reject_manager_request
│
├─── [GET] /update_employee_skill
│                 ├─── [PUT] /add_employee_skill
│                 └─── [PUT] /replace_employee_skill
│
├─── [GET] /manager_request_to_complete_project
│                 ├─── [PUT] /approve_completion_of_project
│                 └─── [DELETE] /reject_completion_of_project
│
├─── [GET] /remove_worker
│                 ├─── [DELETE] /remove_manager
│                 └─── [DELETE] /remove_employee
│
└─── [POST] /admin_logout
```

## Manager
```bash
manager_router.py
│
├─── [GET] /manager_login
│                 └─── [POST] /manager_login
│
├─── [GET] /manager_home
│
├─── [GET] /comprehensive_info
│                
├─── [GET] /filter_employees
│                 └─── [POST] /filter_employees
│
├─── [GET] /project_manager_have
│
├─── [GET] /update_project_status
│                 └─── [PUT] /update_project_status
│
└─── [POST] /manager_logout

```

## Employee
```bash
emp_router.py
│
├─── [GET] /employee_login
│               └─── [POST] /employee_login
│
├─── [GET] /employee_home
│
├─── [GET] /all_colleague
│                
├─── [GET] /update_skill_as_employee
│                ├─── [PUT] /replace_skills
│                └─── [PUT] /add_skills
│
└─── [POST] /employee_logout

```