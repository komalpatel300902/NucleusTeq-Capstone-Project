function validateCredential() {
    // Example: Send a POST request to the backend to accept the request with the given ID
    
    const username_field = document.getElementById("username")
    const password_field = document.getElementById("password")
    const username = username_field.value ;
    const password = password_field.value ;
    console.log(password)
    console.log(username)

    fetch('/employee_login_data', {
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
            window.location.href = '/employee_home';
        } else {
            // If login fails, handle error (e.g., show error message)
            if (response.status === 401) {
                // Unauthorized - show error message
                alert('Invalid username or password');
                window.location.href = '/employee_login';
            } else {
                // Other errors - log to console
                console.error('Login failed:', response.statusText);
            }
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