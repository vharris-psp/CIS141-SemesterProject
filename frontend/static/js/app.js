
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    try {
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
  
      if (response.ok) {
        const responseData = await response.json();
        localStorage.setItem('authToken', responseData.token);
        updateOutput('Login successful!');
        window.location.href = '/dashboard.html'; // Redirect to another page after login
      } else {
        updateOutput('Login failed: ' + response.statusText);
      }
    } catch (err) {
      updateOutput('Error: ' + err.message);
    }
  }