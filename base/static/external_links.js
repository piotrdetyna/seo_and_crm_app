let csrfToken = null;
let siteId = null;

function sendPUTRequest(url, requestData, onSuccess) {
    try {
        fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(requestData),
        }).then(response => {

            if (response.ok) {
                onSuccess();
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

        sendPUTRequest('/find-external/', {'site_id': siteId, 'to_exclude': toExclude }, () => {
            location.reload();
        });
        setInterval(updateProgress, 500, `/external-links-progress/${siteId}/`, findLinksButton);
    };

    
    checkAvailabilityButton.onclick = () => {
        const externalLinksId = checkAvailabilityButton.dataset.externalLinksId;
        checkAvailabilityButton.classList.add('disabled');
        findLinksButton.classList.add('disabled');

        sendPUTRequest('/check-linked-page-availability/', { external_links_id: externalLinksId }, () => {
            location.reload();
        });
        setInterval(updateProgress, 500, `/external-links-progress/${siteId}/`, progressTracker);
    };
});
