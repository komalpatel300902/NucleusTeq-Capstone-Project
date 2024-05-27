function logout(){

    fetch('/admin_logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            // Request accepted successfully, you can update the UI as needed
            // location.reload()
            window.location.href = '/admin_login';
        } else {
            // If login fails, handle error (e.g., show error message)
            if (response.status === 401) {
                // Unauthorized - show error message
                alert('Invalid username or password');
                window.location.href = '/admin_login';
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