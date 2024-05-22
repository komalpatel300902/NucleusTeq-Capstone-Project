function unassignEmployeeProject(empId) {
    // Here you can implement the logic for assigning a project to an employee
    fetch("/unassign_employee_from_project" , {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        },
        // You can optionally send data in the request body if needed
        body: JSON.stringify({ emp_id: empId })
    })
    .then(response => {
        // Handle the response, maybe refresh the page or update UI as needed
        location.reload()
        console.log('Request accepted successfully');
    })
    .catch(error => {
        // Handle errors, show error message or log the error
        console.error('Error accepting request:', error);
    });
}

function unassignManagerProject(managerId) {
     // Here you can implement the logic for assigning a project to an employee
    const project = document.getElementById("project-"+managerId)
    var projectId = project.value;
     fetch("/unassign_manager_from_project" , {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        },
        // You can optionally send data in the request body if needed
        body: JSON.stringify({ manager_id: managerId , project_id: projectId })
    })
    .then(response => {
        // Handle the response, maybe refresh the page or update UI as needed
        location.reload()
        console.log('Request accepted successfully');
    })
    .catch(error => {
        // Handle errors, show error message or log the error
        console.error('Error accepting request:', error);
    });
}