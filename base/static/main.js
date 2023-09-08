async function setCurrentSite(site_id) {
    const response = await fetch('/api/set-current-site/', {
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

    //if next parameter is present in URL, redirect to next page

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    console.log(urlParams)
    const nextSite = urlParams.get('next')
    if (nextSite) {
        window.location.href = nextSite;
    }
    else {
        location.reload()
    }
}

async function getSite(site_id) {
    const response = await fetch(`/api/get-sites/${site_id}/`, {
        method: 'GET',
    })

    if (!response.ok) {
        throw new Error(`Error while fetching site ${site_id}. Status: ${response.status}`);
    }
    const data = await response.json();
    return data

}



async function populateSitesList() {
    let sitesLists = document.querySelectorAll('.sites-list');
    const response = await fetch('/api/get-sites/', {
        method: 'GET',
    });
    if (!response.ok) {
        throw new Error(`Error while fetching sites list. Status: ${response.status}`);
    }
    const data = await response.json();

    sitesLists.forEach(sitesList => {
        data.forEach((site) => {
            let siteElement = document.createElement("span");
            siteElement.dataset.id = site.id;
            siteElement.textContent = site.url;
            siteElement.classList.add('site-list-element');
            siteElement.onclick = () => { setCurrentSite(site.id) };

            let siteLogoElement = document.createElement("img");
            siteLogoElement.src = site.logo;
            siteLogoElement.classList.add('miniature');

            siteElement.insertBefore(siteLogoElement, siteElement.firstChild);
            sitesList.appendChild(siteElement);
        });
    });
}



document.addEventListener('DOMContentLoaded', () => {
    (async () => {
        let currentSiteSpan = document.querySelector('#current-site-url')
        let currentSiteId = currentSiteSpan.dataset.id
        if (currentSiteId) {
            let current_site = await getSite(currentSiteId)
            currentSiteSpan.innerHTML = `Aktualna strona: <a href="/site/"> ${current_site.url}✏️</a>`
        } 
        else {
            currentSiteSpan.innerText = 'Wybierz stronę'
        }
    })();
    
    
    populateSitesList()
})