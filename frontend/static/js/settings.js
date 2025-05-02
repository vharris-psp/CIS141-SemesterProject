document.addEventListener('DOMContentLoaded', () => {    
  
    fetchDeviceConfigs();
  });




async function login() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
}

function addAuthTokenToRequest(headers) {
  const token = sessionStorage.getItem('authToken');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}


async function populate_device_config_elements(device_list) {
  console.log(device_list);
}
async function get_device_info() {
    console.log('Fetching device info...');
    //fetch('/settings/get_device_info')
    //    .then(response => response.json())
    //    .then(data => {
    //        document.getElementById('device_info').innerText = JSON.stringify(data, null, 2);
    //    })
    //    .catch(error => {
    //        console.error('Error fetching device info:', error);
    //    });
    try {
      const response = await fetch('/settings/get_device_info', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      const responseData = await response.json();
      await fet(responseData);
    } catch (err) {
      console.log('Error: ' + err.message);
    } 
}
async function fetchDeviceConfigs() {
  const device_config_collapsible = $('[id^="configcollapsible_"]');
  try {
    const response = await fetch('/settings/get_device_configs', {
      method: 'GET',
      headers: addAuthTokenToRequest({ 'Content-Type': 'application/json' })
    });
    const responseData = await response.json();

    if (responseData.error) {
      console.error('Error fetching device configurations:', responseData.error);
      return;
    }

    const container = document.getElementById('device-config-container');
    if (container) {
      container.innerHTML = responseData.html;
    } else {
      console.error('Device config container not found in the DOM.');
    }
  } catch (error) {
    console.error('Error fetching device configurations:', error);
  }
}
