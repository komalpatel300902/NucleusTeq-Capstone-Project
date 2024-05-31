function validateCredential() {
    // Example: Send a POST request to the backend to accept the request with the given ID

    const username_field = document.getElementById("username")
    const password_field = document.getElementById("password")
    const username = username_field.value ;
    const password = password_field.value ;
    console.log(password)
    console.log(username)

    const response = fetch('/admin_login_data', {
        method: 'POST',
        body: JSON.stringify({ username: username , password: password}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            // Request accepted successfully, you can update the UI as needed
            // location.reload()
            window.location.href = '/admin_home';
        } else {
            // If login fails, handle error (e.g., show error message)
            alert('Invalid username or password');
            location.reload()
           
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
    
}
function preventEnterKeySubmission(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
    }
}
document.addEventListener("DOMContentLoaded", function () {
    const username_field = document.getElementById("username")
    const password_field = document.getElementById("password")
    const submit_button = document.getElementById("submit_button")
    // If you want to prevent submission for all input fields in the form
    username_field.addEventListener("keydown", preventEnterKeySubmission);
    password_field.addEventListener("keydown", preventEnterKeySubmission);
    submit_button.addEventListener("keydown", preventEnterKeySubmission);

    // If you want to prevent submission for specific input fields
    // var specificInput = document.getElementById("specificInputId");
    // specificInput.addEventListener("keydown", preventEnterKeySubmission);
});