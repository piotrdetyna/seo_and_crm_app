let selectedSite = null
let selectedCategory = null

async function addContract() {
    const response = await fetch('/api/add-contract/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            'site_id': selectedSite,
            'payment_frequency': document.querySelector('#payment-frequency').value,
            'value': document.querySelector('#value').value,
            'category': selectedCategory,
            'payment_date': document.querySelector('#payment-date').value,
        })
    })
    return response.ok
}

function handleCheckboxChange(event) {
    let clickedContainer = event.currentTarget
    const clickedCheckbox = event.target;
    if (clickedContainer.classList.contains('clients-list')) {
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

function handleToggleAddContractContainer(addContractContainer) {
    addContractContainer.style.display = addContractContainer.style.display == 'none' ? null : 'none'
}

document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('.clients-list').addEventListener('change', handleCheckboxChange);
    document.querySelector('.categories-list').addEventListener('change', handleCheckboxChange);

    let addContractContainer = document.querySelector('#add-contract-container')
    addContractContainer.style.display = 'none'
    let toggleAddContractContainer = document.querySelector('#add-contract-container-toggle')
    toggleAddContractContainer.onclick = () => { handleToggleAddContractContainer(addContractContainer) }


    let addContractButton = document.querySelector('#add-contract')
    addContractButton.onclick = async () => {
        let response = await addContract()
        let addContractMessage = document.querySelector('#add-contract-message')
        if (response) {
            addContractMessage.innerHTML = 'Dodano umowę.'
            location.reload()
        }
        else {
            addContractMessage.innerHTML = 'Coś poszło nie tak.'
        }
    }
})