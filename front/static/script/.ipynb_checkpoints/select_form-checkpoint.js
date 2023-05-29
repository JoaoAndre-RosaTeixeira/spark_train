document.getElementById('data-form').addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission
            
            const formData = new FormData(this);
            fetch('/select_data', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Error: ' + response.status);
                }
            })
            .then(json => {
                console.log(json);
                // Process the response data
            })
            .catch(error => {
                console.error(error);
            });
        });

