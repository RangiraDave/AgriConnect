// add_product.js

function setSubmitEnabled(enabled) {
  document.getElementById('submit-btn').disabled = !enabled;
}

function setWarningVisible(visible, message = '') {
  const warningDiv = document.getElementById('geoloc-warning');
  const messageSpan = document.getElementById('geoloc-message');
  if (!warningDiv || !messageSpan) {
    console.error('Warning elements not found');
    return;
  }
  warningDiv.classList.toggle('d-none', !visible);
  if (message) {
    messageSpan.textContent = message;
  }
}

function updateLocationDisplay(lat, lng) {
  const locationDisplay = document.getElementById('location-display');
  if (!locationDisplay) {
    console.error('Location display element not found');
    return;
  }
  locationDisplay.value = `${lat}, ${lng}`;
  locationDisplay.classList.add('is-valid');
}

function clearLocationDisplay() {
  const locationDisplay = document.getElementById('location-display');
  if (!locationDisplay) {
    console.error('Location display element not found');
    return;
  }
  locationDisplay.value = '';
  locationDisplay.classList.remove('is-valid');
}

function setLocationStatus(type, message) {
  const statusDiv = document.getElementById('location-status');
  if (!statusDiv) {
    console.error('Location status element not found');
    return;
  }
  if (type === 'success') {
    statusDiv.innerHTML = `<span class="text-success"><i class="fas fa-check-circle me-1"></i>${message}</span>`;
  } else if (type === 'error') {
    statusDiv.innerHTML = `<span class="text-warning"><i class="fas fa-exclamation-triangle me-1"></i>${message}</span>`;
  } else {
    statusDiv.innerHTML = message;
  }
}

function getLocation() {
  console.log('Getting location...');
  const locationDisplay = document.getElementById('location-display');
  if (!locationDisplay) {
    console.error('Location display element not found');
    return;
  }
  
  locationDisplay.value = 'Getting your location...';
  locationDisplay.classList.remove('is-valid');
  setWarningVisible(false);

  if (navigator.geolocation) {
    console.log('Geolocation supported');
    navigator.geolocation.getCurrentPosition(
      (position) => {
        console.log('Position received:', position);
        const lat = position.coords.latitude.toFixed(6);
        const lng = position.coords.longitude.toFixed(6);

        const latField = document.getElementById('id_latitude');
        const lngField = document.getElementById('id_longitude');
        
        if (!latField || !lngField) {
          console.error('Location fields not found');
          return;
        }

        latField.value = lat;
        lngField.value = lng;
        updateLocationDisplay(lat, lng);
        setWarningVisible(false);
        setLocationStatus('success', `Location detected: (${lat}, ${lng})`);
      },
      (error) => {
        console.error('Geolocation error:', error);
        let errorMessage = '';
        switch(error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = 'Location permission denied. You can still add the product, but buyers may not find it easily.';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = 'Location information unavailable. You can still add the product.';
            break;
          case error.TIMEOUT:
            errorMessage = 'Location request timed out. Try again.';
            break;
          default:
            errorMessage = 'Unable to get your location. Try again.';
        }
        clearLocationDisplay();
        setWarningVisible(true, errorMessage);
        setLocationStatus('error', errorMessage);
        
        const latField = document.getElementById('id_latitude');
        const lngField = document.getElementById('id_longitude');
        if (latField && lngField) {
          latField.value = '';
          lngField.value = '';
        }
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
      }
    );
  } else {
    console.error('Geolocation not supported');
    clearLocationDisplay();
    setWarningVisible(true, 'Geolocation is not supported by your browser.');
    setLocationStatus('error', 'Geolocation is not supported by your browser.');
  }
}

document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM loaded, initializing location functionality...');
  const getLocationBtn = document.getElementById('get-location');
  const retryLocationBtn = document.getElementById('retry-geoloc');
  
  if (getLocationBtn) {
    console.log('Get location button found');
    getLocationBtn.addEventListener('click', function(e) {
      e.preventDefault();
      getLocation();
    });
  } else {
    console.error('Get location button not found');
  }
  
  if (retryLocationBtn) {
    console.log('Retry location button found');
    retryLocationBtn.addEventListener('click', function(e) {
      e.preventDefault();
      getLocation();
    });
  }
});