function assignEmployeeProject(empId) {
    // Send an AJAX request to your FastAPI backend to accept the request with the given ID
    // You can use fetch API or any other library like Axios for making AJAX requests
    const selectField = document.getElementById("project-"+empId);
    const projectId = selectField.value;
    fetch("/assign_employee_a_project" , {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        },
        // You can optionally send data in the request body if needed
        body: JSON.stringify({ emp_id: empId, project_id: projectId })
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

function assignManagerProject(manager_id) {
    // Here you can implement the logic for assigning a project to a manager
    const selectField = document.getElementById("project-"+manager_id);
    const projectId = selectField.value;
    fetch("/assign_manager_a_project" , {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        },
        // You can optionally send data in the request body if needed
        body: JSON.stringify({ manager_id: manager_id , project_id: projectId })
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