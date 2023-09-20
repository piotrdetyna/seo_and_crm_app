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
            'invoice_frequency': document.querySelector('#invoice-frequency').value,
            'value': document.querySelector('#value').value,
            'category': selectedCategory,
            'invoice_date': document.querySelector('#invoice-date').value,
            'days_before_invoice_date_to_mark_urgent': document.querySelector('#days-before-invoice-date-to-mark-urgent').value,
        })
    })
    return response.ok
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
            response = await updateIsPaidAttribute(button.dataset.invoiceId)
            if (response) {
                location.reload()
            }
            else {
                button.innerHTML = 'Coś poszło nie tak.'
            }
        }
    })
})