function sendForm() {
    let username = document.querySelector('#username').value
    let password = document.querySelector('#password').value

    fetch('/api/session/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            'username': username,
            'password': password,
        })
    })
    .then(response => {
        if (response.ok) {
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            const nextSite = urlParams.get('next')
            if (nextSite) {
                window.location.href = nextSite;
            }
            else {
                window.location.href = '/';
            }
        }
        else {
            response.json().then(data => {
                document.querySelector('#login-message').innerHTML = 'Nieprawidłowe dane'
            })
            
        }
    })
}


document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#send-form').onclick = () => {
        sendForm()
    }
})