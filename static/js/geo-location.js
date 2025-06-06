// Geo Location Helper Functions
console.log('geo-location.js loaded');

// These variables will be set from Django template for translation
// Fallback to English if not set
const GEOLOC_TXT_UNSUPPORTED = window.GEOLOC_TXT_UNSUPPORTED || 'Geolocation is not supported by your browser.';
const GEOLOC_TXT_DETECTED = window.GEOLOC_TXT_DETECTED || 'Location detected:';
const GEOLOC_TXT_UNABLE = window.GEOLOC_TXT_UNABLE || 'Unable to retrieve location.';
const GEOLOC_TXT_DENIED = window.GEOLOC_TXT_DENIED || 'Location permission denied. You can still add the product without location.';
const GEOLOC_TXT_ENABLE = window.GEOLOC_TXT_ENABLE || 'Please enable location access for this site in your browser settings.';
const GEOLOC_TXT_UNAVAILABLE = window.GEOLOC_TXT_UNAVAILABLE || 'Location information is unavailable. You can still add the product without location.';
const GEOLOC_TXT_TIMEOUT = window.GEOLOC_TXT_TIMEOUT || 'The request to get user location timed out. You can still add the product without location.';
const GEOLOC_TXT_UNKNOWN = window.GEOLOC_TXT_UNKNOWN || 'An unknown error occurred while fetching location. You can still add the product without location.';

function initGeoLocation() {
    const statusDiv = document.getElementById('location-status');
    const latitudeInput = document.getElementById('id_latitude');
    const longitudeInput = document.getElementById('id_longitude');

    if (!statusDiv || !latitudeInput || !longitudeInput) {
        // Elements not found, skip geolocation
        console.log('Geolocation elements not found.');
        return;
    }

    if (!navigator.geolocation) {
        statusDiv.innerHTML = `<i class="fas fa-times-circle text-danger me-1"></i>${GEOLOC_TXT_UNSUPPORTED}`;
        console.log('Geolocation is not supported by your browser');
        return;
    }

    navigator.geolocation.getCurrentPosition(
        success => {
            const lat = success.coords.latitude.toFixed(6);
            const lng = success.coords.longitude.toFixed(6);
            latitudeInput.value = lat;
            longitudeInput.value = lng;

            statusDiv.innerHTML = `<i class="fas fa-check-circle text-success me-1"></i>${GEOLOC_TXT_DETECTED} (${lat}, ${lng})`;
        },
        error => {
            console.warn('Geolocation error:', error);
            let errorMessage = GEOLOC_TXT_UNABLE;
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    errorMessage = `${GEOLOC_TXT_DENIED}<br><small>${GEOLOC_TXT_ENABLE}</small>`;
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMessage = GEOLOC_TXT_UNAVAILABLE;
                    break;
                case error.TIMEOUT:
                    errorMessage = GEOLOC_TXT_TIMEOUT;
                    break;
                case error.UNKNOWN_ERROR:
                    errorMessage = GEOLOC_TXT_UNKNOWN;
                    break;
            }
            statusDiv.innerHTML = `<i class="fas fa-exclamation-triangle text-warning me-1"></i>${errorMessage}`;
        },
        {
            enableHighAccuracy: true,
            timeout: 10000, // Increased timeout slightly
            maximumAge: 60000
        }
    );
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('initGeoLocation called');
    initGeoLocation();
});
