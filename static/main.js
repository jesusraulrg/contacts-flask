const contactsForm = document.querySelector('#contactsForm');

let contacts = []
let editing = false;
let contactId = null

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('/contacts');
    const data = await response.json()
    contacts = data
    renderContact(contacts)
});

function renderContact(contacts){
    const contactsList = document.querySelector('#contactsList')
    contactsList.innerHTML = ''

    contacts.forEach(contact => {
        const contactItem = document.createElement('li')
        contactItem.classList = 'list-group-item list-group-item-light my-2'
        contactItem.innerHTML = `
        <header class="d-flex justify-content-between align-items-center">
            <h3>${contact.nombre} ${contact.apellidos}</h3>
            <div>
                <button class="btn-edit btn btn-success btn-m">Editar</button>
                <button class="btn-delete btn btn-danger btn-m">Eliminar</button>
            </div>
        </header>
        <p class="lead">Email: ${contact.email}</p>
        <p class="lead">Teléfono: ${contact.telefono}</p>
        `

        const btnDelete = contactItem.querySelector('.btn-delete')

        btnDelete.addEventListener('click', async () => {
            const response = await fetch(`/contacts/${contact.id}`, {
                method: 'DELETE'
            })
            const data = await response.json()
            
            contacts = contacts.filter(contact => contact.id !== data.id)
            renderContact(contacts)
        })


        const btnEdit = contactItem.querySelector('.btn-edit')

        btnEdit.addEventListener('click', async (e) => {

            const response = await fetch(`/contacts/${contact.id}`,)
            const data = await response.json()

            contactsForm['nombre'].value = data.nombre;
            contactsForm['apellidos'].value = data.apellidos;
            contactsForm['email'].value = data.email;
            contactsForm['telefono'].value = data.telefono;

            editing = true;
            contactId = data.id;

        })

        contactsList.append(contactItem)
    });

}


contactsForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const nombre = contactsForm['nombre'].value;
    const apellidos = contactsForm['apellidos'].value;
    const email = contactsForm['email'].value;
    const telefono = contactsForm['telefono'].value;

    if (!editing) {
        const response = await fetch('/contacts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre,
                apellidos,
                email,
                telefono
            })
        });
    
        const data = await response.json();
    
        contacts.unshift(data)   
    } else {
        const response = await fetch(`/contacts/${contactId}`,{
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre,
                apellidos,
                email,
                telefono
            }),
        });

        const updatedContact = await response.json();
        contacts = contacts.map(contact => contact.id == updatedContact.id ? updatedContact: contact);
        editing = false
        contactId = null
    }

    renderContact(contacts)
    contactsForm.reset();
});

