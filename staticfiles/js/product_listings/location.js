// Location Dropdowns Management
function initLocationDropdowns() {
    const provinceSelect = document.getElementById('province');
    const districtSelect = document.getElementById('district');
    const sectorSelect = document.getElementById('sector');
    const cellSelect = document.getElementById('cell');
    const villageSelect = document.getElementById('village');

    // Load initial values if they exist
    const selectedProvince = "{{ selected_province }}";
    const selectedDistrict = "{{ selected_district }}";
    const selectedSector = "{{ selected_sector }}";
    const selectedCell = "{{ selected_cell }}";
    const selectedVillage = "{{ selected_village }}";

    if (selectedProvince) {
        loadDistricts(provinceSelect.value, districtSelect).then(() => {
            if (selectedDistrict) {
                loadSectors(districtSelect.value, sectorSelect).then(() => {
                    if (selectedSector) {
                        loadCells(sectorSelect.value, cellSelect).then(() => {
                            if (selectedCell) {
                                loadVillages(cellSelect.value, villageSelect);
                            }
                        });
                    }
                });
            }
        });
    }

    // Event listeners for location dropdowns
    provinceSelect.addEventListener('change', function() {
        const provinceId = this.value;
        resetDropdowns(districtSelect, sectorSelect, cellSelect, villageSelect);
        
        if (provinceId) {
            loadDistricts(provinceId, districtSelect);
        }
    });

    districtSelect.addEventListener('change', function() {
        const districtId = this.value;
        resetDropdowns(sectorSelect, cellSelect, villageSelect);
        
        if (districtId) {
            loadSectors(districtId, sectorSelect);
        }
    });

    sectorSelect.addEventListener('change', function() {
        const sectorId = this.value;
        resetDropdowns(cellSelect, villageSelect);
        
        if (sectorId) {
            loadCells(sectorId, cellSelect);
        }
    });

    cellSelect.addEventListener('change', function() {
        const cellId = this.value;
        resetDropdowns(villageSelect);
        
        if (cellId) {
            loadVillages(cellId, villageSelect);
        }
    });
}

// Helper function to reset dropdowns
function resetDropdowns(...dropdowns) {
    dropdowns.forEach(dropdown => {
        dropdown.innerHTML = `<option value="">${dropdown.dataset.placeholder || 'Select...'}</option>`;
        dropdown.disabled = true;
    });
}

// Functions to load location data
async function loadDistricts(provinceId, districtSelect) {
    try {
        districtSelect.disabled = true;
        const response = await fetch(`/api/districts/?province=${provinceId}`);
        if (!response.ok) {
            throw new Error('Failed to load districts');
        }
        const districts = await response.json();
        
        districtSelect.innerHTML = '<option value="">----------</option>';
        districts.forEach(district => {
            const option = document.createElement('option');
            option.value = district.id;
            option.textContent = district.name;
            // Check if the district should be pre-selected
            const selectedDistrict = document.getElementById('district').dataset.initialValue;
            if (district.id == selectedDistrict) {
                option.selected = true;
            }
            districtSelect.appendChild(option);
        });
        districtSelect.disabled = false;
        // Trigger change event if a district was pre-selected to load dependent dropdowns
        if (districtSelect.value) {
            districtSelect.dispatchEvent(new Event('change'));
        }
    } catch (error) {
        console.error('Error loading districts:', error);
        showError('Failed to load districts. Please try again.');
        districtSelect.disabled = true;
    }
}

async function loadSectors(districtId, sectorSelect) {
    try {
        sectorSelect.disabled = true;
        const response = await fetch(`/api/sectors/?district=${districtId}`);
        if (!response.ok) {
            throw new Error('Failed to load sectors');
        }
        const sectors = await response.json();
        
        sectorSelect.innerHTML = '<option value="">----------</option>';
        sectors.forEach(sector => {
            const option = document.createElement('option');
            option.value = sector.id;
            option.textContent = sector.name;
            const selectedSector = document.getElementById('sector').dataset.initialValue;
             if (sector.id == selectedSector) {
                 option.selected = true;
            }
            sectorSelect.appendChild(option);
        });
        sectorSelect.disabled = false;
        if (sectorSelect.value) {
            sectorSelect.dispatchEvent(new Event('change'));
        }
    } catch (error) {
        console.error('Error loading sectors:', error);
        showError('Failed to load sectors. Please try again.');
        sectorSelect.disabled = true;
    }
}

async function loadCells(sectorId, cellSelect) {
    try {
        cellSelect.disabled = true;
        const response = await fetch(`/api/cells/?sector=${sectorId}`);
        if (!response.ok) {
            throw new Error('Failed to load cells');
        }
        const cells = await response.json();
        
        cellSelect.innerHTML = '<option value="">----------</option>';
        cells.forEach(cell => {
            const option = document.createElement('option');
            option.value = cell.id;
            option.textContent = cell.name;
            const selectedCell = document.getElementById('cell').dataset.initialValue;
             if (cell.id == selectedCell) {
                 option.selected = true;
            }
            cellSelect.appendChild(option);
        });
        cellSelect.disabled = false;
         if (cellSelect.value) {
            cellSelect.dispatchEvent(new Event('change'));
        }
    } catch (error) {
        console.error('Error loading cells:', error);
        showError('Failed to load cells. Please try again.');
        cellSelect.disabled = true;
    }
}

async function loadVillages(cellId, villageSelect) {
    try {
        villageSelect.disabled = true;
        const response = await fetch(`/api/villages/?cell=${cellId}`);
        if (!response.ok) {
            throw new Error('Failed to load villages');
        }
        const villages = await response.json();
        
        villageSelect.innerHTML = '<option value="">----------</option>';
        villages.forEach(village => {
            const option = document.createElement('option');
            option.value = village.id;
            option.textContent = village.name;
             const selectedVillage = document.getElementById('village').dataset.initialValue;
             if (village.id == selectedVillage) {
                 option.selected = true;
            }
            villageSelect.appendChild(option);
        });
        villageSelect.disabled = false;
    } catch (error) {
        console.error('Error loading villages:', error);
        showError('Failed to load villages. Please try again.');
        villageSelect.disabled = true;
    }
}

// Function to show error messages
function showError(message) {
    // This function needs to be available globally or passed down
    // For now, let's log it to console as well
    console.error('Frontend Error:', message);
    // You might want to display this in a user-friendly way in your HTML
    // e.g., appending to a dedicated error message area.
}
