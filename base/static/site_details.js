document.addEventListener('DOMContentLoaded', () => {
    


    let siteForm = document.querySelector('form#edit-site')
    let siteId = siteForm.dataset.siteId
    siteForm.onsubmit = (event) => {
        event.preventDefault()
        let siteFormData = new FormData(siteForm);  
        siteFormData.append('site_id', siteId)
      
        fetch('/edit-site/', {
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
})