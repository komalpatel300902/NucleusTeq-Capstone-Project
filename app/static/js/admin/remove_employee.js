document.addEventListener("DOMContentLoaded", function() {
    // Attach click event listener to all remove manager buttons
    var removeManagerButtons = document.querySelectorAll(".removeManagerButton");
    removeManagerButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            var managerId = button.getAttribute("data-manager-id");
            removeManager(managerId);
        });
    });

    // Attach click event listener to all remove employee buttons
    var removeEmployeeButtons = document.querySelectorAll(".removeEmployeeButton");
    removeEmployeeButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            var empId = button.getAttribute("data-emp-id");
            removeEmployee(empId);
        });
    });
});

function removeManager(managerId) {
    // Send an AJAX request to your FastAPI backend to remove the manager
    // You can use fetch API or any other library like Axios for making AJAX requests
    fetch(`/remove_manager?manager_id=${managerId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        }
    })
    .then(response => {
        if (response.ok) {
            // Handle success
            console.log('Manager removed successfully');
            // Optionally, refresh the page or update UI as needed
        } else {
            // Handle errors
            console.error('Failed to remove manager');
        }
    })
    .catch(error => {
        // Handle network errors
        console.error('Error:', error);
    });
}

function removeEmployee(empId) {
    // Send an AJAX request to your FastAPI backend to remove the employee
    // You can use fetch API or any other library like Axios for making AJAX requests
    fetch(`/remove_employee?emp_id=${empId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        }
    })
    .then(response => {
        if (response.ok) {
            // Handle success
            console.log('Employee removed successfully');
            // Optionally, refresh the page or update UI as needed
        } else {
            // Handle errors
            console.error('Failed to remove employee');
        }
    })
    .catch(error => {
        // Handle network errors
        console.error('Error:', error);
    });
}
