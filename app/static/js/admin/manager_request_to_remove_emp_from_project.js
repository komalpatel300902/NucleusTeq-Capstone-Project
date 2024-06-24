function acceptRequest(empId,projectId,managerId) {
    // Send an AJAX request to your FastAPI backend to accept the request with the given ID
    // You can use fetch API or any other library like Axios for making AJAX requests
    fetch("/accept_manager_request_to_unassign_emp_from_project" , {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        },
        // You can optionally send data in the request body if needed
        body: JSON.stringify({ emp_id: empId, project_id: projectId , manager_id: managerId })
    })
    .then(response => {
        // Handle the response, maybe refresh the page or update UI as needed
        location.reload();
        console.log('Request accepted successfully');
    })
    .catch(error => {
        // Handle errors, show error message or log the error
        console.error('Error accepting request:', error);
    });
}

function rejectRequest(empId,projectId,managerId) {
    // Send an AJAX request to your FastAPI backend to reject the request with the given ID
    fetch('/reject_manager_request_to_unassign_emp_from_project', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        },
        // You can optionally send data in the request body if needed
        body: JSON.stringify({ emp_id: empId, project_id: projectId , manager_id: managerId })
    })
    .then(response => {
        // Handle the response, maybe refresh the page or update UI as needed
        location.reload()
        console.log('Request rejected successfully');
    })
    .catch(error => {
        // Handle errors, show error message or log the error
        console.error('Error rejecting request:', error);
    });
}
