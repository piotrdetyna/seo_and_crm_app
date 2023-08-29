document.addEventListener('DOMContentLoaded', () => {
    const findLinksButton = document.querySelector('#find-links');
    const siteId = findLinksButton.value    
    findLinksButton.onclick = () => {
        findLinksButton.classList.add('disabled')
        let to_exclude = document.querySelector('#to-exclude').value.split(",").map(item => item.trim());
        to_exclude = to_exclude.filter(element => element.trim() !== '');
        fetch('/find-external/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
            },
            body: JSON.stringify({
                'site_id': siteId,
                'to_exclude': to_exclude
            })
        })
        .then(response => {
            if (response.ok) {
                response.json().then(data => {
                    location.reload()
                })

            }
        })
    }


    const checkAvailabilityButton = document.querySelector('#check-availability');
    console.log(checkAvailabilityButton.dataset)
    const externalLinksId = checkAvailabilityButton.dataset.externalLinksId
    checkAvailabilityButton.onclick = () => {
        checkAvailabilityButton.classList.add('disabled')
        console.log(externalLinksId)
        fetch('/check-linked-page-availability/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
            },
            body: JSON.stringify({
                'external_links_id': externalLinksId,
            })
        })
        .then(response => {
            if (response.ok) {
                response.json().then(data => {
                    location.reload()
                })

            }
        })
    }

})