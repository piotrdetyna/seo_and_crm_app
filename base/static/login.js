function sendForm() {
    let username = document.querySelector('#username').value
    let password = document.querySelector('#password').value

    fetch('/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'username': username,
            'password': password,
        })
    })
    .then(response => {
        console.log(response)
    })
}


document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#send-form').onclick = () => {
        sendForm()
    }
})