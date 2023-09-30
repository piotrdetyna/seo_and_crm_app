let selectedSite = null
let selectedCategory = null
let contractId = null

async function editContract() {
    const response = await fetch(`/api/contracts/${contractId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            'site_id': selectedSite,
            'invoice_frequency': document.querySelector('#invoice-frequency').value,
            'value': document.querySelector('#value').value,
            'category': selectedCategory,
            'invoice_date': document.querySelector('#invoice-date').value,
            'days_before_invoice_date_to_mark_urgent': document.querySelector('#days-before-invoice-date-to-mark-urgent').value,
        })
    })
    return response.ok
}

async function deleteContract() {
    const response = await fetch(`/api/contracts/${contractId}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
    })
    return response.ok
}

function handleCheckboxChange(event) {

    let clickedContainer = event.currentTarget
    const clickedCheckbox = event.target;
    if (clickedContainer.id == 'sites-list') {
        selectedSite = clickedCheckbox.value
    } 
    else {
        selectedCategory = clickedCheckbox.value
    }
    
    if (clickedCheckbox.checked) {
        const checkboxes = event.currentTarget.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            if (checkbox !== clickedCheckbox) {
                checkbox.checked = false;
            }
        });
    }
}


document.addEventListener('DOMContentLoaded', () => {

    let sitesList = document.querySelector('#sites-list')
    sitesList.addEventListener('change', handleCheckboxChange);
    sitesList.querySelectorAll('input').forEach((checkbox) => {
        if (checkbox.checked) {
            selectedSite = checkbox.value
        }
    })
    let categoriesList = document.querySelector('#categories-list')
    categoriesList.addEventListener('change', handleCheckboxChange);
    categoriesList.querySelectorAll('input').forEach((checkbox) => {
        if (checkbox.checked) {
            selectedCategory = checkbox.value
        }
    })
    

    let editContractButton = document.querySelector('#edit-contract')
    contractId = editContractButton.value
    editContractButton.onclick = async () => {
        let response = await editContract()
        let editContractMessage = document.querySelector('#edit-contract-message')
        if (response) {
            editContractMessage.innerHTML = 'Edytowano umowę.'
            location.reload()
        }
        else {
            editContractMessage.innerHTML = 'Coś poszło nie tak.'
        }
    }

    let deleteContractButton = document.querySelector('#delete-contract')
    deleteContractButton.onclick = async () => {
        let response = await deleteContract()
        let deleteContractMessage = document.querySelector('#delete-contract-message')
        if (response) {
            deleteContractMessage.innerHTML = 'Usunięto umowę.'
            window.location.replace("/contracts/");
        }
        else {
            deleteContractMessage.innerHTML = 'Coś poszło nie tak.'
        }
    }

    
})