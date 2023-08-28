async function setCurrentSite(site_id) {
    const response = await fetch('/set-current-site/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            'site_id': site_id,
        })
    })
    if (!response.ok) {
		throw new Error(`Error while fetching sites list. Status: ${response.status}`);
	}
	const data = await response.json();
    location.reload()
}

async function getSite(site_id) {
    const response = await fetch(`/get-sites/${site_id}/`, {
        method: 'GET',
    })

    if (!response.ok) {
        throw new Error(`Error while fetching site ${site_id}. Status: ${response.status}`);
    }
    const data = await response.json();
    return data

}



async function populateSitesList() {
    let sitesList = document.querySelector('#sites-list')
    const response = await fetch('/get-sites/', {
        method: 'GET',
    })
    if (!response.ok) {
		throw new Error(`Error while fetching sites list. Status: ${response.status}`);
	}
	const data = await response.json();

    data.forEach((site) => {
        let siteElement = document.createElement("span");
        siteElement.dataset.id = site.id
        siteElement.textContent = site.url
        siteElement.classList.add('site-list-element')
        siteElement.onclick = () => {setCurrentSite(site.id)}
        
        let siteLogoElement = document.createElement("img");
        siteLogoElement.src = site.logo
        siteLogoElement.classList.add('miniature')

        siteElement.insertBefore(siteLogoElement, siteElement.firstChild);
        sitesList.appendChild(siteElement);
        
    })
}


document.addEventListener('DOMContentLoaded', () => {
    (async () => {
        let currentSiteSpan = document.querySelector('#current-site-url')
        let currentSiteId = currentSiteSpan.dataset.id
        if (currentSiteId) {
            let current_site = await getSite(currentSiteId)
            currentSiteSpan.innerHTML = `Aktualna strona: <a href="/site/${current_site.id}/"> ${current_site.url}✏️</a>`
        } 
        else {
            currentSiteSpan.innerText = 'Wybierz stronę'
        }
    })();
    
    
    populateSitesList()
})