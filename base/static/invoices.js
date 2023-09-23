let selectedContract = null
let selectedContractClient = null

async function addInvoice() {
    let formData = new FormData();
    formData.append('contract_id', selectedContract);
    formData.append('invoice_file', document.querySelector('#invoice-file').files[0]);
    let report_file = document.querySelector('#report-file').files[0]
    if (report_file) {
        formData.append('report_file', report_file);
    }
    

    const response = await fetch('/api/add-invoice/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: formData
    });

    return response.ok;
}

function handleCheckboxChange(event) {
    const clickedCheckbox = event.target;
    selectedContract = clickedCheckbox.value
    selectedContractClient = clickedCheckbox.dataset.clientId
    document.querySelector('#get-client-info-button').classList.remove('disabled')
    
    if (clickedCheckbox.checked) {
        const checkboxes = event.currentTarget.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            if (checkbox !== clickedCheckbox) {
                checkbox.checked = false;
            }
        });
    }
}

async function updateIsPaidAttribute(invoiceId, value) {
    const response = await fetch(`/api/edit-invoice/${invoiceId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            'is_paid': value,
        })
    })
    return response.ok
}


async function getClientInfo() {
    const response = await fetch(`/api/get-client-info/${selectedContractClient}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
    })
    return response
}


document.addEventListener('DOMContentLoaded', () => {
    let changeIsPaidAttributeButtons = document.querySelectorAll('.change-is-paid')
    changeIsPaidAttributeButtons.forEach(button => {
        button.onclick = async () => {
            let invoiceId = button.parentNode.parentNode.dataset.invoiceId
            value = button.dataset.isPaid == 'True' ? false : true
            
            response = await updateIsPaidAttribute(invoiceId, value)
            if (response) {
                location.reload()
            }
            else {
                button.innerHTML = 'Coś poszło nie tak.'
            }
        }
    })

    let contractsList = document.querySelector('#contracts-list')
    if (contractsList) {
        contractsList.addEventListener('change', handleCheckboxChange);
    } else {
        selectedContract = document.querySelector('#info-contract-id').dataset.contractId
        selectedContractClient = document.querySelector('#info-client-id').dataset.clientId
        document.querySelector('#get-client-info-button').classList.remove('disabled')
    }

    let addInvoiceContainer = document.querySelector('#add-invoice-container')
    addInvoiceContainer.style.display = 'none'
    let toggleAddInvoiceContainerButton = document.querySelector('#add-invoice-toggle-button')
    toggleAddInvoiceContainerButton.onclick = () => {
        addInvoiceContainer.style.display = addInvoiceContainer.style.display == 'none' ? null : 'none'
    }

    let addInvoiceButton = document.querySelector('#add-invoice-button')
    addInvoiceButton.onclick = async () => {
        let response = await addInvoice()
        if (response) {
            document.querySelector('#add-invoice-message').innerHTML = 'Dodano fakturę.'
            location.reload()
        }
        else {
            document.querySelector('#add-invoice-message').innerHTML = 'Coś poszło nie tak.'
        }
    }

    let getClientInfoButton = document.querySelector('#get-client-info-button')
    let clientInfoCointaner = document.querySelector('#client-info-container')
    getClientInfoButton.onclick = async () => {
        let response = await getClientInfo()
        if (response.ok) {
            client_info = await response.json()
            client_info = client_info.client_info
            
            clientInfoCointaner.innerHTML = ''

            const ul = document.createElement('ul');
            for (const key in client_info) {
            if (client_info.hasOwnProperty(key)) {
                const li = document.createElement('li');
                li.textContent = `${key}: ${client_info[key] !== null ? client_info[key] : 'brak'}`;
                ul.appendChild(li);
            }
            }
            clientInfoCointaner.appendChild(ul);
        }
        else {
            clientInfoCointaner.innerHTML = 'Coś poszło nie tak.'
        }
    }

})