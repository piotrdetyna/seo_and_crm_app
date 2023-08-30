let csrfToken = null;

async function sendRequestAndReload(url, requestData) {
    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(requestData),
        });

        if (response.ok) {
            location.reload();
        } else {
            console.error('Request failed with status:', response.status);
        }
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

document.addEventListener('DOMContentLoaded', () => {
    csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    const findLinksButton = document.querySelector('#find-links');
    findLinksButton.onclick = async () => {
        findLinksButton.classList.add('disabled');
        const siteId = findLinksButton.value;
        const toExclude = getExcludedDomains();
        await sendRequestAndReload('/find-external/', {
            site_id: siteId,
            to_exclude: toExclude,
        });
    };

    const checkAvailabilityButton = document.querySelector('#check-availability');
    checkAvailabilityButton.onclick = async () => {
        checkAvailabilityButton.classList.add('disabled');
        const externalLinksId = checkAvailabilityButton.dataset.externalLinksId;
        await sendRequestAndReload('/check-linked-page-availability/', {
            external_links_id: externalLinksId,
        });
    };
});
