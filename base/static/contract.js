let selectedSite = null
let selectedCategory = null
let contractId = null

async function editContract() {
    const response = await fetch(`/api/edit-contract/${contractId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            'site_id': selectedSite,
            'contract_duration': document.querySelector('#contract-duration').value,
            'payment_frequency': document.querySelector('#payment-frequency').value,
            'value': document.querySelector('#value').value,
            'category': selectedCategory,
        })
    })
    return response.ok
}


function handleCheckboxChange(event) {
    let clickedContainer = event.currentTarget
    const clickedCheckbox = event.target;
    if (clickedContainer.classList.contains('#sites-list')) {
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
})