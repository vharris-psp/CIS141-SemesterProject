document.addEventListener('DOMContentLoaded', () => {    
  
    fetchDevices().then(() => {

    container.find('.accordion').accordion({
      collapsible: true,
      heightStyle: "content"
    
        });
    })
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


// async function populate_device_config_elements(device_list) {
//   console.log(device_list);
// }
// async function get_device_info() {
//     console.log('Fetching device info...');

//     try {
//       const response = await fetch('/settings/get_device_info', {
//         method: 'GET',
//         headers: { 'Content-Type': 'application/json' }
//       });
//       const responseData = await response.json();
//       await fet(responseData);
//     } catch (err) {
//       console.log('Error: ' + err.message);
//     }
// }
async function fetchDevices() {
  const response = await fetch('/settings/get_device_list', );
  const data = await response.json();
  console.log(data)
  
  container = $('.settings-viewer');
  const values = {}
  container.append(data[0])
  for (let i = 0; i < data.length; i++) {
      
      values[data[i].name] = data[i].config;
  }
  container.find('.edit-button[data-device]').each(function () {
    const deviceName = $(this).attr('data-device');
    $(this).on('click', function () {
      save_config(deviceName);
    });
  });
  container.find('.select-input-widget[options]').each(function () {
    const options = $(this).attr('options');
    const select = $(this).find('select');
    const selectOptions = JSON.parse(options);
    for (let i = 0; i < selectOptions.length; i++) {
      const option = selectOptions[i];
      select.append(`<option value="${option}">${option}</option>`);
    }
  })






}

async function fetchWidget(){

}

async function save_config(device_name) {
  const deviceContainer = $(`[data-device="${device_name}"]`);
  const settings = deviceContainer.find('[data-setting]');
  const inputs = {}
  const warning_labels = {}
  let hasChanges = false;

  const deviceSettings = {}; // Create a temporary object to store settings for the device

  settings.each(function () {
    const key = $(this).data('setting');
    
    inputs[key] = $(this).find('input');
    if (inputs[key].length === 0) {
      inputs[key] = $(this).find('select');
    }
    warning_labels[key] = $(this).find('.warning-label');
    const currentValue = inputs[key].val();
    if (!deviceSettings[device_name]) {
      deviceSettings[device_name] = {}; // Initialize the device settings if not already done
    }
    if (deviceSettings[device_name][key] !== currentValue) {
      hasChanges = true;
      deviceSettings[device_name][key] = currentValue; // Update the temporary object
    }
  });

  if (hasChanges) {
    console.log(`Changes detected for device: ${device_name}`);
    const result = await put_changes(device_name, deviceSettings[device_name]);
    
    
   
    console.log(result);
    for (let key in result.successful_changes){
      if (result.successful_changes.hasOwnProperty(key)) {
        const input = $(`[data-setting="${key}"]`).find('input');
        inputs[key].css('border-color', 'green');
        let label = warning_labels[key]
        label.text(result.successful_changes[key]);
        label.attr('class', 'success-label active');
      }
      
        
    } 
    for(let key in result.failed_changes) {
      if (result.failed_changes.hasOwnProperty(key)) {
      const input = $(`[data-setting="${key}"]`).find('input');
      inputs[key].css('border-color', 'red');
      let label = warning_labels[key]
      label.text(result.failed_changes[key]);
      label.attr('class', 'warning-label active');

      };
    }
      
    }
  }
    

    


async function put_changes(device_name, deviceSettings) {
  try {
    const response = await fetch(`/settings/save_device_config/${device_name}`, {
      method: 'PUT', // Change to PUT or the correct method allowed by the server
      headers: addAuthTokenToRequest({
        'Content-Type': 'application/json'
      }),
      body: JSON.stringify(deviceSettings)
    });

    if (!response.ok) {
      throw new Error(`Failed to save settings for device: ${device_name}`);
    }

    const data = await response.json();
    console.log(`Settings successfully saved for device: ${device_name}`, data);
    return data; // Return the parsed JSON response
  } catch (error) {
    console.error(`Error in PUT request for device: ${device_name}`, error);
    return { successful_changes: [], failed_changes: [] }; // Return a default structure in case of error
  }
};