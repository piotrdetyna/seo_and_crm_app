let csrfToken = null;

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

function getExcludedDomains() {
    const toExcludeInput = document.querySelector('#to-exclude');
    const toExclude = toExcludeInput.value
        .split(',')
        .map(item => item.trim())
        .filter(element => element !== '');

    return toExclude;
}

async function fetchData() {
    try {
        const siteId = document.querySelector('#find-links').value;
        const response = await fetch(`/find-external-progress/${siteId}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const data = await response.json();
            const progressElement = document.querySelector('#find-links');
            progressElement.innerHTML = parseInt((data.current / data.target) * 100) + '%';
            console.log(data);
        }
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    const findLinksButton = document.querySelector('#find-links');
    findLinksButton.onclick = async () => {
        findLinksButton.classList.add('disabled');
        const siteId = findLinksButton.value;
        const toExclude = getExcludedDomains();

        sendPUTRequest('/find-external/', {'site_id': siteId, 'to_exclude': toExclude }, () => {
            location.reload();
        });
        setInterval(fetchData, 500);
    };

    const checkAvailabilityButton = document.querySelector('#check-availability');
    checkAvailabilityButton.onclick = async () => {
        checkAvailabilityButton.classList.add('disabled');
        const externalLinksId = checkAvailabilityButton.dataset.externalLinksId;

        sendPUTRequest('/check-linked-page-availability/', { external_links_id: externalLinksId }, () => {
            location.reload();
        });
    };
});
