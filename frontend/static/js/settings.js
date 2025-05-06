document.addEventListener('DOMContentLoaded', () => {    
  
    fetchDevices().then(() => {

    container.find('.accordion').accordion({
      collapsible: true,
      heightStyle: "content"
    });
  });
});
class Device {
  constructor(name, config) {
    this.name = name;
    this.config = config;
  }
}


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
async function fetchDevices() {
  const response = await fetch('/settings/get_device_list', );
  const data = await response.text();
  container = $('.settings-viewer');
  container.append(data);



 


  
}

async function fetchWidget(){

}
