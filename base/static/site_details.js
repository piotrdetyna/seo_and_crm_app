var siteId = null

function editSite(siteForm) {
    let siteFormData = new FormData(siteForm);  
 
    fetch(`/api/sites/${siteId}/`, {
        method: 'PATCH',
        headers: {
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: siteFormData
    })
    .then(response => {
        if (response.ok) {
            document.querySelector('#add-site-message').innerHTML = '<p>Edytowano stronę pomyślnie</p>'
        } else {
            document.querySelector('#add-site-message').innerHTML = '<p>Coś poszło nie tak. Spróbuj ponownie</p>'
        }
    })
}

function deleteSite() {
  
    fetch(`/api/sites/${siteId}/`, {
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
            document.querySelector('#delete-site-message').innerHTML = '<p>Coś poszło nie tak. Spróbuj ponownie</p>'
        }
    })
}


document.addEventListener('DOMContentLoaded', () => {
    let siteForm = document.querySelector('form#edit-site')
    siteId = siteForm.dataset.siteId
    siteForm.onsubmit = (event) => {
        event.preventDefault()
        editSite(siteForm)
    }

    document.querySelector('#delete-site-button').onclick = () => {
        deleteSite()
    }
})