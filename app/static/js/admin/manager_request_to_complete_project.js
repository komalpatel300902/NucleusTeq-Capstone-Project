function approve(projectId) {
    // Here you can implement the logic for assigning a project to an employee
    
    fetch("/approve_completion_of_project?project_id="+projectId , {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        },
        // You can optionally send data in the request body if needed
        // body: JSON.stringify({ manager_id: managerId, project_id: projectId, status: project_status })
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
function reviewAgain(projectId) {
    // Here you can implement the logic for assigning a project to an employee
   
    fetch("/reject_completion_of_project?project_id="+projectId , {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        },
        // You can optionally send data in the request body if needed
        // body: JSON.stringify({ manager_id: managerId, project_id: projectId, status: project_status })
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
