document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Here, you can implement your logic to check the username and password
    // For example, you can check against a predefined set of credentials or validate against a database

    if (username === 'alex_peck' && password === 'AlexIsBest@123') {
        alert('Login successful! Redirecting to dashboard...');
        // Redirect to the successful login page or dashboard
        window.location.href = 'dashboard.html';
    } else {
        alert('Invalid username or password. Please try again.');
    }
});
