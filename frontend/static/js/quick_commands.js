document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('host').value = 'tech-mdf';
    document.getElementById('username').value = 'vharris';
    document.getElementById('password').value = 'password';
    document.getElementById('command').value = 'show run int fi 1/0/1';
  });

document.getElementById('runCommand').addEventListener('click', runCommand);
document.getElementById('testAPI').addEventListener('click', testAPI);

async function testAPI() {
  try {
    const response = await fetch('http://127.0.0.1:5000/test_api', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });
    const responseData = await response.json();
    updateOutput(responseData.message);
  } catch (err) {
    updateOutput('Error: ' + err.message);
  } 
}
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
      localStorage.setItem('authToken', responseData.token); // Use localStorage for cross-page persistence
      updateOutput('Login successful!');
      window.location.href = '/dashboard.html'; // Redirect to another page after login
    } else {
      updateOutput('Login failed: ' + response.statusText);
    }
  } catch (err) {
    updateOutput('Error: ' + err.message);
  }
}

function addAuthTokenToRequest(headers) {
  const token = sessionStorage.getItem('authToken');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

// Modify runCommand to include the token
function runCommand() {
  const host = document.getElementById('host').value;
  const command = document.getElementById('command').value;

  fetch('http://127.0.0.1:5000/send_command', {
    method: 'POST',
    headers: addAuthTokenToRequest({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ host, command })
  })
    .then(res => res.json())
    .then(responseData => {
      document.getElementById('output').textContent = responseData.output;
    })
    .catch(err => {
      document.getElementById('output').textContent = 'Error: ' + err.message;
    });
}
function updateOutput(message) {
  document.getElementById('output').textContent = message;
}
function runCommand() {
    const host = document.getElementById('host').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const command = document.getElementById('command').value;
    
    fetch('http://127.0.0.1:5000/send_command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ host, username, password, command })
    })
    .then(res => res.json())
    .then(responseData => {
      document.getElementById('output').textContent = responseData.output;
    })
    .catch(err => {
      document.getElementById('output').textContent = 'Error: ' + err.message;
    });
  }