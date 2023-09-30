let site_id = null
let notesList = null
let currentNoteContent = null
let currentNoteTitle = null
let currentNote = null
let deleteNoteButton = null
let siteId = null

async function addNote() {
    const response = await fetch('/api/notes/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            'text': currentNoteContent.value,
            'title': currentNoteTitle.value,
            'site_id': siteId,
        })
    })
    if (!response.ok) {
		throw new Error(`Error while adding note. Status: ${response.status}`);
	}
	const data = await response.json();
    return data.note
}

async function getAndSetCurrentNote(noteId) {
    const response = await fetch(`/api/notes/${noteId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    if (!response.ok) {
		throw new Error(`Error while getting note. Status: ${response.status}`);
	}

	let data = await response.json()
    data = data.note
    currentNote.style.display = null
    currentNoteContent.value = data.text
    currentNoteTitle.value = data.title
    currentNote.dataset.noteId = data.id
}

async function saveNote() {
    const response = await fetch(`/api/notes/${currentNote.dataset.noteId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            'text': currentNoteContent.value,
            'title': currentNoteTitle.value,
        })
    })
    if (!response.ok) {
		throw new Error(`Error while saving note. Status: ${response.status}`);
	}
    let notesListElement = notesList.querySelector(`[data-note-id="${currentNote.dataset.noteId}"]`)
    notesListElement.querySelector('strong').innerHTML = currentNoteTitle.value
}

async function deleteNote() {
    const response = await fetch(`/api/notes/${currentNote.dataset.noteId}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        }
    })
    if (!response.ok) {
		throw new Error(`Error while deleting note. Status: ${response.status}`);
	}
	notesList.querySelector(`[data-note-id="${currentNote.dataset.noteId}"]`).remove()
    currentNote.style.display = 'none'
}


document.addEventListener('DOMContentLoaded', () => {
    currentNoteContent = document.querySelector('#current-note-content')
    currentNoteTitle = document.querySelector('#current-note-title')
    currentNote = document.querySelector('.note')
    notesList = document.querySelector('.notes-list')
    deleteNoteButton = document.querySelector('#delete-current-note')
    siteId = document.querySelector('#info').dataset.siteId

    notesList.addEventListener('click', async (event) => {
        const notesListItem = event.target.closest('.notes-list-item');
        if (notesListItem) {
            getAndSetCurrentNote(notesListItem.dataset.noteId);
            deleteNoteButton.style.display = null;
        }
    });
    

    let saveNoteButton = document.querySelector('#save-current-note')
    saveNoteButton.onclick = async () => {
        if (currentNote.dataset.noteId){
            saveNote()
        }
        else {
            newNoteInfo = await addNote()
            
            const newNoteItem = document.createElement('li');
            newNoteItem.classList.add('notes-list-item');
            newNoteItem.setAttribute('data-note-id', newNoteInfo.id);
            const strongElement = document.createElement('strong');
            strongElement.textContent = newNoteInfo.title;
            const smallElement = document.createElement('small');
            smallElement.textContent = ' ' + newNoteInfo.date;
            newNoteItem.appendChild(strongElement);
            newNoteItem.appendChild(smallElement);

            notesList.appendChild(newNoteItem);
            deleteNoteButton.style.display = null
            currentNote.dataset.noteId = newNoteInfo.id
        }
    }

    deleteNoteButton.onclick = () => {
        deleteNote()
    }

    let addNoteButton = document.querySelector('#add-note')
    addNoteButton.onclick = () => {
        currentNote.dataset.noteId = ''
        currentNoteTitle.value = ''
        currentNoteContent.value = ''
        deleteNoteButton.style.display = 'none'
        currentNote.style.display = null
    }
})
