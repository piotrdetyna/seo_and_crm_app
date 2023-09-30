let sidebar = null
let main = null
let toggleSidebarBtn = null

async function setCurrentSite(siteId) {
    const response = await fetch(`/api/session/current-site/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            'site_id': siteId,
        })
    })
    if (!response.ok) {
		throw new Error(`Error while fetching sites list. Status: ${response.status}`);
	}
	const data = await response.json();

    //if next parameter is present in URL, redirect to next page

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const nextSite = urlParams.get('next')
    if (nextSite) {
        window.location.href = nextSite;
    }
    else {
        location.reload()
    }
}

async function getSite(site_id) {
    const response = await fetch(`/api/sites/${site_id}/`, {
        method: 'GET',
    })

    if (!response.ok) {
        throw new Error(`Error while fetching site ${site_id}. Status: ${response.status}`);
    }
    let data = await response.json();
    return data['site']
}


async function logout() {
    const response = await fetch(`/api/logout/`, {
        method: 'DELETE',
        headers: {'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value},
    })

    if (!response.ok) {
        throw new Error(`Error while logging out. Status: ${response.status}`);
    }
    else {
        location.reload()
    }
}


async function populateSitesList() {
    let sitesLists = document.querySelectorAll('.sites-list');
    const response = await fetch('/api/sites/', {
        method: 'GET',
    });
    if (!response.ok) {
        throw new Error(`Error while fetching sites list. Status: ${response.status}`);
    }
    let data = await response.json();
    data = data['sites']

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

function handleResize() {
    if (window.innerWidth < 767 && !sidebar.classList.contains('sidebar-hidden')) {
        toggleSidebarBtn.click()
    }
    else if (window.innerWidth > 767 && sidebar.classList.contains('sidebar-hidden')) {
        toggleSidebarBtn.click()
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    sidebar = document.querySelector('aside')
    main = document.querySelector('main')
    toggleSidebarBtn = document.getElementById('menu-button');

    toggleSidebarBtn.onclick = () => {
        sidebar.classList.toggle('sidebar-hidden')
        main.classList.toggle('main-full-width')
    }
    
    window.addEventListener("resize", handleResize)
    handleResize()

    let currentSiteSpan = document.querySelector('#current-site-url')
    let currentSiteId = currentSiteSpan.dataset.id
    if (currentSiteId) {
        let current_site = await getSite(currentSiteId)
        currentSiteSpan.innerHTML = `Aktualna strona: <a href="/site/"> ${current_site.url}✏️</a>`
    } 
    else {
        currentSiteSpan.innerText = 'Brak wybranej strony'
    }
    document.querySelector('#logout-button').onclick = () => { logout() }

    
    populateSitesList()
})