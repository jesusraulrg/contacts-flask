const contactsForm = document.querySelector('#contactsForm');

contactsForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const nombre = contactsForm['nombre'].value;
    const apellidos = contactsForm['apellidos'].value;
    const email = contactsForm['email'].value;
    const telefono = contactsForm['telefono'].value;

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
    console.log(data);

    contactsForm.reset();
});