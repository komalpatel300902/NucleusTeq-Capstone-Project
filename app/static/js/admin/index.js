document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    if (form) {
        form.addEventListener('submit', async function(event) {
            const username_field = document.getElementById("username")
            const password_field = document.getElementById("password")
            const username = username_field.value ;
            const password = password_field.value ;
            console.log(password)
            console.log(username)

            fetch('/admin_login_data', {
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
                    console.log("I am inside reponse.ok");
                    window.location.href = '/admin_home';
                    
                    
                } else {
                    // If login fails, handle error (e.g., show error message)
                    console.log("I am inside else block ");
                    alert('Invalid username or password');
                    window.location.href = '/admin_login';
                    
                
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        })
    }       
});

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