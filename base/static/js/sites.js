function checkExpiry() {
  
    fetch(`/api/sites/expiry/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
    })
    .then(response => {
        if (response.ok) {
            location.reload()
        } else {
            document.querySelector('#check-expiry').innerHTML = 'Coś poszło nie tak. Sprawdź poprawność domeny'
        }
    })
}



document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#check-expiry').onclick = () => {
        document.querySelector('#check-expiry').classList.add('disabled')
        checkExpiry()
    }
})