let csrfToken = null;
let siteId = null;

function findExternalLinks(requestData) {
    try {
        fetch(`/api/external-links-managers/${siteId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(requestData),
        }).then(response => {

            if (response.ok) {
                //location.reload()
            } else {
                console.error('Request failed with status:', response.status);
            }
        })
    } catch (error) {
        console.error('An error occurred:', error);
    }
}


function checkLinkedPagesAvaliability() {
    try {
        fetch(`/api/external-links-managers/${siteId}/status/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        }).then(response => {

            if (response.ok) {
                location.reload()
            } else {
                console.error('Request failed with status:', response.status);
            }
        })
    } catch (error) {
        console.error('An error occurred:', error);
    }
}


function updateProgress(url, progressElement) {
    try {
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => {
            if (response.ok) {
                response.json().then(data => {
                    progressElement.innerHTML = parseInt((data.current / data.target) * 100) + '%';
                })
            }
        })
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

function getExcludedDomains() {
    const toExcludeInput = document.querySelector('#to-exclude');
    const toExclude = toExcludeInput.value
        .split(',')
        .map(item => item.trim())
        .filter(element => element !== '');

    return toExclude;
}

document.addEventListener('DOMContentLoaded', () => {
    csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    siteId = document.querySelector('#find-links').value;

    const checkAvailabilityButton = document.querySelector('#check-availability');
    
    const progressTracker = document.querySelector('#check-availability-progres')
    const findLinksButton = document.querySelector('#find-links');

    findLinksButton.onclick = () => {
        findLinksButton.classList.add('disabled');
        if (checkAvailabilityButton) {
            checkAvailabilityButton.classList.add('disabled');
        }
        const toExclude = getExcludedDomains();

        findExternalLinks({'to_exclude': toExclude })
        setInterval(updateProgress, 500, `/api/external-links-managers/${siteId}/?attributes=progress_current,progress_target`, findLinksButton);
    };

    
    checkAvailabilityButton.onclick = () => {
        const externalLinksId = checkAvailabilityButton.dataset.externalLinksId;
        checkAvailabilityButton.classList.add('disabled');
        findLinksButton.classList.add('disabled');

        checkLinkedPagesAvaliability();
        setInterval(updateProgress, 500, `/api/external-links-managers/${siteId}/?attributes=progress_current,progress_target`, progressTracker);
    };
});
