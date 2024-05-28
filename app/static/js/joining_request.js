
alert('JavaScript file is linked correctly!');
console.log("js linked correctly");
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('employeeRegistrationForm');

    if (form) {
        form.addEventListener('submit', async function(event) {
            console.log("i am in register employees");
            event.preventDefault(); // Prevent the default form submission

            const formData = new FormData(form);
            const data = {};

            formData.forEach((value, key) => {
                data[key] = value;
            });
            // location.reload();
            const jsonData = JSON.stringify(data);
            console.log(jsonData)
            try {
                const response = await fetch('/register_form_submission', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: jsonData
                });

                if (response.ok) {
                    alert('Form submitted successfully!');
                    
                } else {
                    alert('Form submission failed.');
                    if (response.status === 422) {
                        // Unauthorized - show error message
                        alert("Password must be alpha Numeric \n Email must bolong organization ")
                        window.location.href = '/registration_form';
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred during form submission.');
            }
        });
    } else {
        console.error('Form not found!');
    }
});
