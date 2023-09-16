let siteId = null

async function addBacklink(linking_page) {
    const response = await fetch('/api/add-backlink/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            'linking_page': linking_page,
            'site_id': siteId,
        })
    })
    return response.ok
}

async function deleteBacklink(backlink_id) {
    const response = await fetch('/api/delete-backlink/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            'backlink_id': backlink_id,
        })
    })
    return response.ok
}

async function checkBacklinksStatus() {
    const response = await fetch('/api/check-backlinks-status/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            'site_id': siteId,
        })
    })
    return response.ok
}

document.addEventListener('DOMContentLoaded', () => {
    let addBacklinkButton = document.querySelector('#add-backlink')
    siteId = addBacklinkButton.value

    addBacklinkButton.onclick = async () => {
        let linking_page = document.querySelector('#linking-page').value
        response = await addBacklink(linking_page)

        if (response) {
            location.reload()
        }
        else {
            document.querySelector('#add-backlink-message').innerHTML = 'Coś poszło nie tak'
        }
    }

    deleteBacklinkButtons = document.querySelectorAll('.delete-backlink-button')
    deleteBacklinkButtons.forEach(button => {
        button.onclick = async () => {
            response = await deleteBacklink(button.dataset.id)
            if (response) {
                location.reload()
            }
            else {
                button.innerHTML = 'Coś poszło nie tak'
            }
        }
    })


    checkStatusButton = document.querySelector('#check-status-button')
    checkStatusMessage = document.querySelector('#check-status-message')
    checkStatusButton.onclick = async () => {
        checkStatusButton.classList.add('disabled')
        checkStatusMessage.innerHTML = 'Proszę czekać... | '
        if (checkBacklinksStatus()) {
            /*setTimeout(() => {
                location.reload();
            }, 4000);*/
            
        }
        else {
            checkStatusMessage.innerHTML = 'Coś poszło nie tak | '
        }
    }
})