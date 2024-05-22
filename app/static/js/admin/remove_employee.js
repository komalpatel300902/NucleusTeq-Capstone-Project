

function removeManager(managerId) {
    // Send an AJAX request to your FastAPI backend to remove the manager
    // You can use fetch API or any other library like Axios for making AJAX requests
    fetch(`/remove_manager`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        },
        body: JSON.stringify({manager_id: managerId})
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

function removeEmployee(empId) {
    // Send an AJAX request to your FastAPI backend to remove the employee
    // You can use fetch API or any other library like Axios for making AJAX requests
    fetch(`/remove_employee`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        },
        body: JSON.stringify({emp_id: empId})
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
