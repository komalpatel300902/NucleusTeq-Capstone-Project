// Function to handle form submission
function submitForm() {
    // Prevent the default form submission
    event.preventDefault();
    
    // Get form data
    var formData = new FormData(document.getElementById("projectForm"));
    
    // You can now handle the form data as needed, for example, send it to the server via AJAX
    // Example using fetch API:
    fetch("/submit", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (response.ok) {
            // Handle success
            console.log("Form submitted successfully");
            // Optionally, redirect to another page or perform other actions
        } else {
            // Handle errors
            console.error("Form submission failed");
        }
    })
    .catch(error => {
        // Handle network errors
        console.error("Error:", error);
    });
}

// Attach event listener to the submit button
document.getElementById("submitButton").addEventListener("click", submitForm);
 