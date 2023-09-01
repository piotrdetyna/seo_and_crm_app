let site_id = null
let currentNoteContent = null
let currentNoteTitle = null
let currentNote = null

async function addNote(text) {
    const response = await fetch('/add-note/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            'text': text,
            'site_id': site_id,
        })
    })
    if (!response.ok) {
		throw new Error(`Error while adding note. Status: ${response.status}`);
	}
	const data = await response.json();
}

async function getAndSetCurrentNote(noteId) {
    const response = await fetch(`/get-note/${noteId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    if (!response.ok) {
		throw new Error(`Error while adding note. Status: ${response.status}`);
	}
	const data = await response.json();
    currentNoteContent.value = data.text
    currentNoteTitle.value = data.title
    currentNote.dataset.noteId = data.id
}

async function saveNote() {
    const response = await fetch('/update-note/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            'text': currentNoteContent.value,
            'title': currentNoteTitle.value,
            'note_id': currentNote.dataset.noteId,
        })
    })
    if (!response.ok) {
		throw new Error(`Error while adding note. Status: ${response.status}`);
	}
	const data = await response.json();
    console.log(data)
}


document.addEventListener('DOMContentLoaded', () => {
    currentNoteContent = document.querySelector('#current-note-content')
    currentNoteTitle = document.querySelector('#current-note-title')
    currentNote = document.querySelector('.note')

    let notesListItems = document.querySelectorAll('.notes-list-item')
    notesListItems.forEach(notesListItem => {
        notesListItem.onclick = async () => {
            console.log(notesListItem.dataset.noteId)
            getAndSetCurrentNote(notesListItem.dataset.noteId)
        }
    })


    let saveNoteButton = document.querySelector('#save-current-note')
    saveNoteButton.onclick = () => {
        saveNote()
    }
})
