document.addEventListener('DOMContentLoaded', () => {

  });

document.getElementById('runCommand').addEventListener('click', runCommand);
document.getElementById('testAPI').addEventListener('click', testAPI);



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