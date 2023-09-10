var siteId = null

function editSite(siteForm) {
    let siteFormData = new FormData(siteForm);  
    siteFormData.append('site_id', siteId)
  
    fetch('/api/edit-site/', {
        method: 'PUT',
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
  
    fetch('/api/delete-site/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({'site_id': siteId})
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