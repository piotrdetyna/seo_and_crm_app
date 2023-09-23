let invoiceId = null
let currentDisplayed = 'invoice'

async function editInvoice() {
    let formData = new FormData();

    let invoiceFile = document.querySelector('#invoice-file').files[0]
    if (invoiceFile) {
        formData.append('invoice_file', invoiceFile);
    }
    
    let reportFile = document.querySelector('#report-file').files[0]
    let deleteReportFileElement = document.querySelector('#delete-report')
        
    deleteReportFile = false
    if (deleteReportFileElement) {
        if (deleteReportFileElement.checked) {
            deleteReportFile = true
        }
    }
    if (reportFile && !deleteReportFile) {
        formData.append('report_file', reportFile);
    }
    if (deleteReportFile) {
        formData.append('report_file', null);
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


async function getInvoiceFile() {
    const response = await fetch(`/api/invoice-get-file/${invoiceId}/invoice_file/`, {
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
    return blob
}


async function getReportFile() {
    const response = await fetch(`/api/invoice-get-file/${invoiceId}/report_file/`, {
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
    return blob
}


async function handleSwitch() {
    currentDisplayed = currentDisplayed == 'invoice' ? 'report' : 'invoice'
    document.querySelector('#displayed-file-type').innerHTML = currentDisplayed == 'report' ? 'Raport' : 'Faktura'
    if (currentDisplayed == 'invoice') {
        blob = await getInvoiceFile()
    }
    else {
        blob = await getReportFile()
    }
    if (blob) {
        const pdfUrl = URL.createObjectURL(blob);
        document.getElementById('pdf-embed').src = pdfUrl;
    }
}


document.addEventListener('DOMContentLoaded', async () => {
    let switchDisplayedFileElement = document.getElementById("switch-input")
    switchDisplayedFileElement.addEventListener("change", handleSwitch)
    let ediInvoiceButton = document.querySelector('#edit-invoice')
    invoiceId = ediInvoiceButton.value

    blob = await getInvoiceFile()
    if (blob) {
        const pdfUrl = URL.createObjectURL(blob);
        document.getElementById('pdf-embed').src = pdfUrl;
    }

    
    let editInvoiceMessage = document.querySelector('#edit-invoice-message')
    
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
    let downloadInvoiceMessage = document.querySelector('#download-invoice-message')
    downloadInvoiceButton.onclick = async () => {
        blob = await getInvoiceFile()
        
        if (!blob) {
            downloadInvoiceMessage.innerHTML = 'Coś poszło nie tak.'
        }
        else {
            downloadFile(blob, `invoice_${invoiceId}.pdf`)  
        }
    }

    let downloadReportButton = document.querySelector('#download-report')
    let downloadReportMessage = document.querySelector('#download-report-message')
    downloadReportButton.onclick = async () => {
        blob = await getInvoiceFile()
        
        if (!blob) {
            downloadReportMessage.innerHTML = 'Coś poszło nie tak.'
        }
        else {
            downloadFile(blob, `report_${invoiceId}.pdf`)  
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