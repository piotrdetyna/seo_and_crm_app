function handleSwitch() {
    if (this.checked) {
        document.querySelector('#client-type').innerHTML = 'Osoba prywatna'
        document.querySelector('#nip').style.display = 'none'
        document.querySelector('#address').style.display = null
        document.querySelector('#full-name').style.display = null
    } else {
        document.querySelector('#client-type').innerHTML = 'Firma'
        document.querySelector('#nip').style.display = null
        document.querySelector('#address').style.display = 'none'
        document.querySelector('#full-name').style.display = 'none'
    }
}



document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#address').style.display = 'none'
    document.querySelector('#full-name').style.display = 'none'
    document.getElementById("switchInput").addEventListener("change", handleSwitch)

    let form = document.querySelector('form#add-client')
    form.onsubmit = (event) => {
        event.preventDefault()
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        let clientName = data['name'];

        fetch('/api/add-client/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                console.log(response)
                response.json().then(data => {
                    clientId = data.client.id
                    console.log(clientName, clientId)
                    form.style.pointerEvents = 'none';
                    document.querySelector('#add-client-message').innerHTML =  '<p>Dodano klienta. Teraz możesz dodać stronę.</p>'
                    const label = document.createElement('label');
                    const clients = document.querySelector('.clients-list');
                    const input = document.createElement('input');
                    input.type = 'checkbox';
                    input.value = clientId;
                    label.appendChild(input);
                    label.appendChild(document.createTextNode(clientName));
                    clients.appendChild(label);
                    input.click()

                })
            } else {
                document.querySelector('#add-client-message').innerHTML = '<p>Coś poszło nie tak. Spróbuj ponownie</p>'
            }
        })

    }

    const toggleContainers = (showChoice) => {
        document.querySelector('#client-choice-container').style.display = showChoice ? 'block' : 'none';
        document.querySelector('#client-add-container').style.display = showChoice ? 'none' : 'block';
    }
    
    document.querySelector('#add-client-button').onclick = () => toggleContainers(false);
    document.querySelector('#choice-client-button').onclick = () => toggleContainers(true);


    function handleCheckboxChange(event) {
        const clickedCheckbox = event.target;
        
        if (clickedCheckbox.checked) {
            const checkboxes = document.querySelectorAll('.clients-list input[type="checkbox"]');
            checkboxes.forEach(checkbox => {
                if (checkbox !== clickedCheckbox) {
                    checkbox.checked = false;
                }
            });
        }
    }

    document.querySelector('.clients-list').addEventListener('change', handleCheckboxChange);

    const addSiteForm = document.getElementById("add-site");
    const clientsListContainer = document.querySelector(".clients-list");

    clientsListContainer.addEventListener("change", function(event) {
        if (event.target.type === "checkbox") {
            let isClientSelected = false;
            const clientsList = clientsListContainer.querySelectorAll("input[type='checkbox']");

            clientsList.forEach(function(checkbox) {
                if (checkbox.checked) {
                    isClientSelected = true;
                }
            });

            if (isClientSelected) {
                addSiteForm.style.pointerEvents = 'auto';
            } else {
                addSiteForm.style.pointerEvents = 'none';
            }
        }
    });

    function getSelectedCheckboxValue() {
        const checkboxes = document.querySelectorAll('.clients-list input[type="checkbox"]');
        
        for (const checkbox of checkboxes) {
            if (checkbox.checked) {
                return checkbox.value;
            }
        }
        
        return 'Brak';
    }

    let siteForm = document.querySelector('form#add-site')
    siteForm.onsubmit = (event) => {
        event.preventDefault()
        let siteFormData = new FormData(siteForm);        
        siteFormData.append('client_id', getSelectedCheckboxValue())

        fetch('/api/add-site/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
            },
            body: siteFormData
        })
        .then(response => {
            if (response.ok) {
                document.querySelector('#add-site-message').innerHTML = '<p>Dodano stronę pomyślnie</p>'
            } else {
                document.querySelector('#add-site-message').innerHTML = '<p>Coś poszło nie tak. Spróbuj ponownie</p>'
            }
        })
    }
})