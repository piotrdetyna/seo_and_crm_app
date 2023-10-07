let selectedContract = null
let selectedContractClient = null

async function addInvoice() {
    let formData = new FormData();
    formData.append('contract_id', selectedContract);
    formData.append('payment_date', document.querySelector('#invoice-payment-date').value);
    formData.append('invoice_file', document.querySelector('#invoice-file').files[0]);
    let report_file = document.querySelector('#report-file').files[0]
    if (report_file) {
        formData.append('report_file', report_file);
    }
    

    const response = await fetch('/api/invoices/', {
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
    const response = await fetch(`/api/invoices/${invoiceId}/`, {
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


async function updateOverduityAttribute() {
    const response = await fetch(`/api/invoices/overduity/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
    })
    return response.ok
}


async function getClientInfo() {
    const response = await fetch(`/api/clients/${selectedContractClient}/?api=true`, {
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

    let checkOverduityButton = document.querySelector('#check-invoices-overduity')
    checkOverduityButton.onclick = async () => {
        let response = await updateOverduityAttribute()
        if (response) {
            checkOverduityButton.innerHTML = 'Sprawdzono zaległość faktur.'
            location.reload()
        }
        else {
            checkOverduityButton.innerHTML = 'Coś poszło nie tak.'
        }
    }

    let getClientInfoButton = document.querySelector('#get-client-info-button')
    let clientInfoCointaner = document.querySelector('#client-info-container')
    getClientInfoButton.onclick = async () => {
        let response = await getClientInfo()
        clientInfoCointaner.innerHTML = ''
        if (response.ok) {
            let client_info = await response.json()
            client = client_info.client
            company = client_info.company
            clientInfoCointaner.innerHTML = ''

            let ul = document.createElement('ul');
            for (const key in client) {
                if (client.hasOwnProperty(key)) {
                    const li = document.createElement('li');
                    li.textContent = `${key}: ${client[key] !== null ? client[key] : 'brak'}`;
                    ul.appendChild(li);
                }
            }
            clientInfoCointaner.appendChild(ul);
            const hr = document.createElement('hr');
            clientInfoCointaner.appendChild(hr)
            ul = document.createElement('ul');
            for (const key in company) {
                if (company.hasOwnProperty(key)) {
                    const li = document.createElement('li');
                    li.textContent = `${key}: ${company[key] !== null ? company[key] : 'brak'}`;
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