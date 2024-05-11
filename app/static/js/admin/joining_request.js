function acceptRequest(requestId) {
    // Example: Send a POST request to the backend to accept the request with the given ID
    fetch('/accept_joining_request', {
        method: 'POST',
        body: JSON.stringify({ requestId: requestId }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            // Request accepted successfully, you can update the UI as needed
            console.log('Request accepted successfully');
        } else {
            // Error handling
            console.error('Failed to accept request');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function rejectRequest(requestId) {
    // Example: Send a POST request to the backend to reject the request with the given ID
    fetch('/reject_joining_request', {
        method: 'POST',
        body: JSON.stringify({ requestId: requestId }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            // Request rejected successfully, you can update the UI as needed
            console.log('Request rejected successfully');
        } else {
            // Error handling
            console.error('Failed to reject request');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
