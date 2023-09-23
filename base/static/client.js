let clientId = null
let isClientCompany = null


function editClient(clientForm) {
    let clientFormData = new FormData(clientForm);  
    clientFormData.append('is_company', isClientCompany)
 
    fetch(`/api/edit-client/${clientId}/`, {
        method: 'PATCH',
        headers: {
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: clientFormData
    })
    .then(response => {
        if (response.ok) {
            document.querySelector('#edit-client-message').innerHTML = '<p>Edytowano klienta pomyślnie</p>'
        } else {
            document.querySelector('#edit-client-message').innerHTML = '<p>Coś poszło nie tak. Spróbuj ponownie</p>'
        }
    })
}

function deleteClient() {
  
    fetch(`/api/delete-client/${clientId}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
    })
    .then(response => {
        if (response.ok) {
            window.location.replace("/");
        } else {
            document.querySelector('#delete-client-message').innerHTML = '<p>Coś poszło nie tak. Spróbuj ponownie</p>'
        }
    })
}

function handleSwitch() {
    const isPrivate = this.checked;
    document.querySelector('#client-type').innerHTML = isPrivate ? 'Osoba prywatna' : 'Firma';
    document.querySelector('#nip').style.display = isPrivate ? 'none' : null;
    document.querySelector('#address').style.display = isPrivate ? null : 'none';
    document.querySelector('#full-name').style.display = isPrivate ? null : 'none';
    isClientCompany = !isPrivate;
}


document.addEventListener('DOMContentLoaded', () => {
    let switchElement = document.getElementById("switchInput")
    isClientCompany = switchElement.checked
    switchElement.addEventListener("change", handleSwitch)
    switchElement.click()
    switchElement.click()
    let clientForm = document.querySelector('#edit-client')
    clientId = clientForm.dataset.clientId
    clientForm.onsubmit = (event) => {
        event.preventDefault()
        editClient(clientForm)
    }

    let deleteClientButton = document.querySelector('#delete-client-button')
    deleteClientButton.onclick = () => {
        deleteClient()
    }
    


})