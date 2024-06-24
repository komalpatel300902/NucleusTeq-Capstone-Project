async function requestForEmployeesRemoval(empId, projectId){
    // You can use fetch API or any other library like Axios for making AJAX requests
    const manger_idField = document.getElementById("manager_id");
    const manager_id = manger_idField.value;
    console.log(manager_id, projectId, empId);
    try{
    const response = await fetch("/request_admin_to_unassign_emp_from_project" , {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        },
        // You can optionally send data in the request body if needed
        body: JSON.stringify({ emp_id: empId, project_id: projectId , manager_id: manager_id})
    });
        // Handle the response, maybe refresh the page or update UI as needed
    if (response.ok){
            alert("Request send Successfully");
        }else{
            alert("Request Failed");
            if (response.status === 422){
                const errorDetails = await response.json();
                alert(errorDetails.detail);
            }
        }
        location.reload()
        console.log('Request accepted successfully');
    }
    catch(error) {
        // Handle errors, show error message or log the error
        console.error('Error accepting request:', error);
    }
}

async function filterEmployee(){
    const selectField = document.getElementById("searchInput");
    
    const emp_name= manger_idField.value;
    fetch("/request_admin_to_unassign_emp_from_project?emp_name="+emp_name , {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        },
        // You can optionally send data in the request body if needed
        // body: JSON.stringify({ skill : skill})
    })
    .then(response => {
        // Handle the response, maybe refresh the page or update UI as needed
        location.reload()
        console.log('Filtered record successfully');
    })
    .catch(error => {
        // Handle errors, show error message or log the error
        console.error('Error accepting request:', error);
    });
}