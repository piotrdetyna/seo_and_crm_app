async function addKeyword() {
    let siteId = document.querySelector('#add-keyword').value
    let keyword = document.querySelector('#keyword-input').value

    const response = await fetch('/api/keywords/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            'keyword': keyword,
            'site_id': siteId,
        })
    })
    data = await response.json()
    if (!data) {
        return false
    }
    return data.keywords.position
}


async function checkKeywordPosition(keyword) {
    const response = await fetch(`/api/keywords/${keyword}/position/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
    })
    data = await response.json()
    if (!data) {
        return false
    }
    return data.keywords[0].position
}


async function deleteKeyword(keyword) {
    const response = await fetch(`/api/keywords/${keyword}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
    })
    return response.ok
}


document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#reload').onclick = () => {
        location.reload()
    }
    let overlay = document.querySelector('.overlay')
    let keywordInput = document.querySelector('#keyword-input')
    let addKeywordButton = document.querySelector('#add-keyword')
    
    let keywords = []
    
    let keywordListItemsSelector = document.querySelectorAll('.keywords-list-item')
    keywordListItemsSelector.forEach((keywordListItem) => {
        keywords.push({
            'keyword': keywordListItem.innerHTML,
            'id': keywordListItem.dataset.keywordId,
        })
        keywordListItem.onclick = () => {
            keywordInput.value = keywordListItem.innerHTML
        }
    })

    addKeywordButton.onclick = async () => {
        addKeywordButton.classList.add('disabled')
        let keywordToAdd = keywordInput.value
        let keywordToAddExists = false
        let existingKeywordId = 0
        keywords.forEach((keyword) => {
            if (keyword.keyword == keywordToAdd) {
                keywordToAddExists = true
                existingKeywordId = keyword.id
            }
        })
        let position = null
        addKeywordButton.innerHTML = 'Proszę czekać...'
        if (keywordToAddExists) {
            position = await checkKeywordPosition(existingKeywordId)
        }
        else {
            position = await addKeyword()
        }

        if (position) {
            document.querySelector('#checked-position').innerHTML = position
            overlay.style.display = null
        }
        else {
            document.querySelector('#add-keyword-message').innerHTML = 'Zablokowano przez Google'
        }
    }

    document.querySelectorAll('.delete-keyword').forEach((keywordObject) => {
        keywordObject.onclick = async () => {
            responseOk = await deleteKeyword(keywordObject.dataset.keywordId)
            if (responseOk) {
                location.reload()
            }
            else {
                keywordObject.innerHTML += ' Coś poszło nie tak.'
            }
        }
    })

    document.querySelectorAll('.check-position').forEach((keywordObject) => {
        keywordObject.onclick = async () => {
            let keywordToCheck = ''
            keywords.forEach((keyword) => {
                if (keyword.id == keywordObject.dataset.keywordId) {
                    keywordToCheck = keyword.keyword
                }
            })
            keywordInput.value = keywordToCheck
            addKeywordButton.click()
        }
    })

})