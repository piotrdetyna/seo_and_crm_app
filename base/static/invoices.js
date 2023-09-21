let selectedContract = null

async function addContract() {
    const response = await fetch('/api/add-contract/', {
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

async function addInvoice() {
    let formData = new FormData();
    formData.append('contract_id', selectedContract);
    formData.append('invoice_file', document.querySelector('#invoice-file').files[0]);
    let report_file = document.querySelector('#report-file').files[0]
    if (!report_file) {
        report_file = null
    }
    formData.append('report_file', report_file);

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
    
    if (clickedCheckbox.checked) {
        const checkboxes = event.currentTarget.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            if (checkbox !== clickedCheckbox) {
                checkbox.checked = false;
            }
        });
    }
}



async function updateIsPaidAttribute(invoiceId) {
    const response = await fetch(`/api/change-invoice-is-paid/${invoiceId}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
    })
    return response.ok
}


document.addEventListener('DOMContentLoaded', () => {
    let changeIsPaidAttributeButtons = document.querySelectorAll('.change-is-paid')
    changeIsPaidAttributeButtons.forEach(button => {
        button.onclick = async () => {
            let invoiceId = button.parentNode.parentNode.dataset.invoiceId
            response = await updateIsPaidAttribute(invoiceId)
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

})