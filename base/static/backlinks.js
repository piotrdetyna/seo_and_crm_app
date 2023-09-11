let siteId = null

async function addBacklinks(linking_page) {
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
    if (!response.ok) {
		throw new Error(`Error while adding backlink. Status: ${response.status}`);
	}
	const data = await response.json();
    return data
}

document.addEventListener('DOMContentLoaded', () => {
    let addBacklinkButton = document.querySelector('#add-backlink')
    siteId = addBacklinkButton.value

    addBacklinkButton.onclick = async () => {
        let linking_page = document.querySelector('#linking-page').value
        console.log(addBacklinks(linking_page))
    }
})