function addSkills(empId) {
    // Here you can implement the logic for assigning a project to an employee
    const field = document.getElementById("new_skills-"+empId)
    const skills = field.value;
    fetch("/add_skill" , {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        },
        // You can optionally send data in the request body if needed
        body: JSON.stringify({ emp_id: empId, skills: skills })
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

function replaceSkills(empId) {
    // Here you can implement the logic for assigning a project to a manager

    const field = document.getElementById("new_skills-"+empId)
    const skills = field.value;
    fetch("/replace_skill" , {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        },
        // You can optionally send data in the request body if needed
        body: JSON.stringify({ emp_id: empId, skills:skills})
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