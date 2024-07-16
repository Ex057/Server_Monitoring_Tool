function runTest(url, name, password) {

    var data = {'server':{
        
            'ip_address': url,
            'user_name': name,
            'password': password

    }
    };

    fetch('/monitor/run_test', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Test ran successfully!");
            window.location.reload();  // Reload the page to show the updated results
        } else {
            alert("Failed to run test.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}