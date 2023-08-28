document.addEventListener('DOMContentLoaded', () => {
    const findLinksButton = document.querySelector('#find-links');
    const siteId = findLinksButton.value    
    findLinksButton.onclick = () => {
        let to_exclude = document.querySelector('#to-exclude').value.split(",").map(item => item.trim());
        to_exclude = to_exclude.filter(element => element.trim() !== '');
        console.log(to_exclude)
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
                    console.log(data)
                    document.querySelector('#find-links-message').innerHTML = 'Znaleziono linki, możesz odświeżyć stronę'
                })
                
            }
        })
    }
    const toggleButton = document.getElementById('toggleButton');
    const contentDiv = document.getElementById('accordion-item');
  
    toggleButton.addEventListener('click', () => {
      if (contentDiv.style.display === 'none') {
        contentDiv.style.display = 'block';
        toggleButton.textContent = 'Ukryj zawartość';
      } else {
        contentDiv.style.display = 'none';
        toggleButton.textContent = 'Pokaż zawartość';
      }
    });
})