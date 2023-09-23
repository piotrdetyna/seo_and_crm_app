let invoiceId = null


async function editInvoice() {
    let formData = new FormData();

    let invoiceFile = document.querySelector('#invoice-file').files[0]
    if (invoiceFile) {
        formData.append('invoice_file', invoiceFile);
    }
    
    let reportFile = document.querySelector('#report-file').files[0]
    let deleteReportFile = document.querySelector('#delete-report')
    if (deleteReportFile) {
        if (deleteReportFile.checked) {
            formData.append('report_file', null);
        }
    }
    else if (reportFile) {
        formData.append('report_file', reportFile);
    }

    let isPaid = document.querySelector('#is-paid').checked
    formData.append('is_paid', isPaid);

    const response = await fetch(`/api/edit-invoice/${invoiceId}/`, {
        method: 'PATCH',
        headers: {
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: formData
    });

    return response.ok;
}

async function deleteInvoice() {
    const response = await fetch(`/api/delete-invoice/${invoiceId}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
    })
    return response.ok
}


function downloadFile(blob, filename) {
    let url = window.URL.createObjectURL(blob);
    let a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    
    a.click();
    document.body.removeChild(a);
}


async function downloadInvoiceFile() {
    const response = await fetch(`/api/invoice-download-file/${invoiceId}/invoice_file/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
    })
    if (!response.ok) {
        return false
    }
    let blob = await response.blob();
    downloadFile(blob, `invoice_${invoiceId}.pdf`)  
    return true  
}


async function downloadReportFile() {
    const response = await fetch(`/api/invoice-download-file/${invoiceId}/report_file/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
    })
    if (!response.ok) {
        return false
    }
    let blob = await response.blob();
    downloadFile(blob, `report_${invoiceId}.pdf`)  
    return true  
}


document.addEventListener('DOMContentLoaded', () => {

    let ediInvoiceButton = document.querySelector('#edit-invoice')
    let editInvoiceMessage = document.querySelector('#edit-invoice-message')
    invoiceId = ediInvoiceButton.value
    ediInvoiceButton.onclick = async () => {
        let response = await editInvoice()
        
        if (response) {
            editInvoiceMessage.innerHTML = 'Edytowano fakturę.'
            location.reload()
        }
        else {
            editInvoiceMessage.innerHTML = 'Coś poszło nie tak.'
        }
    }

    let downloadInvoiceButton = document.querySelector('#download-invoice')
    let downloadInvoiceMessage= document.querySelector('#download-invoice-message')
    downloadInvoiceButton.onclick = async () => {
        responseOk = await downloadInvoiceFile()
        if (!responseOk) {
            downloadInvoiceMessage.innerHTML = 'Coś poszło nie tak.'
        }
    }

    let downloadReportButton = document.querySelector('#download-report')
    let downloadReportMessage = document.querySelector('#download-report-message')
    downloadReportButton.onclick = async () => {
        responseOk = await downloadReportFile()
        if (!responseOk) {
            downloadReportMessage.innerHTML = 'Coś poszło nie tak.'
        }
    }

    let deleteInvoiceButton = document.querySelector('#delete-invoice')
    let deleteInvoiceMessage = document.querySelector('#delete-invoice-message')
    deleteInvoiceButton.onclick = async () => {
        responseOk = await deleteInvoice()
        if (responseOk) {
            deleteInvoiceMessage.innerHTML = 'Usunięto fakturę.'
            window.location.replace("/invoices/");
        }
        else {
            deleteInvoiceMessage.innerHTML = 'Coś poszło nie tak.'
        }
    }
    
})