function requestForEmployees(empId){
    // You can use fetch API or any other library like Axios for making AJAX requests
    const selectField = document.getElementById("project-"+empId);
    const projectId = selectField.value;
    fetch("/request_for_employee" , {
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