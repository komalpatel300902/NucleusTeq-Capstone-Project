async function requestForEmployees(empId){
    // You can use fetch API or any other library like Axios for making AJAX requests
    const selectField = document.getElementById("project-"+empId);
    const manger_idField = document.getElementById("manager_id");
    const manager_id = manger_idField.value;
    const projectId = selectField.value;
    try{
    const response = await fetch("/filtered_employee" , {
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
    
    const skill = manger_idField.value;
    fetch("/filtered_employee?skill="+skill , {
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