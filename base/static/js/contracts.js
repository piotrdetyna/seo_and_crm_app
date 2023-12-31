let selectedSite = null
let selectedCategory = null

async function addContract() {
    const response = await fetch('/api/contracts/', {
        method: 'POST',
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


async function checkUrgency() {
    const response = await fetch('/api/contracts/urgency/', {
        method: 'PUT',
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

    let checkUrgencyButton = document.querySelector('#check-urgency-button')
    checkUrgencyButton.onclick = () => {
        let response = checkUrgency()
        if (response) {
            location.reload()
        }
    }
})