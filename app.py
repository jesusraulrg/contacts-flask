from flask import Flask, jsonify, request, send_file
from psycopg2 import connect, extras

app = Flask(__name__)

host = 'localhost'
port = 5432
dbname = 'contacts'
user = 'jesusraulrg'
password = 'DSitMoM.12'


def get_connection():
    conn = connect(host=host, port=port, dbname=dbname, user=user, password=password)
    return conn


@app.route('/')
def home():
    return send_file('static/index.html')


@app.get('/contacts')
def get_contacts():

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM contactos')
    contacts = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(contacts)

@app.post('/contacts')
def create_contact():
    new_contact = request.get_json()
    nombre = new_contact['nombre']
    apellidos = new_contact['apellidos']
    email = new_contact['email']
    telefono = new_contact['telefono']

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor )

    cur.execute('INSERT INTO contactos (nombre, apellidos, email, telefono) VALUES (%s, %s, %s, %s) RETURNING *', (nombre, apellidos, email, telefono))
    new_created_contact = cur.fetchone()
    print(new_created_contact)
    conn.commit()

    cur.close()
    conn.close()

    return jsonify(new_created_contact)

@app.delete('/contacts/<id>')
def delete_contact(id):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('DELETE FROM contactos WHERE id = %s RETURNING *', (id,))
    contact = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if contact is None:
        return jsonify({'message': 'Contact not found'}), 404
    return jsonify(contact)

@app.put('/contacts/<id>')
def update_contact(id):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    new_contact = request.get_json()
    nombre = new_contact['nombre']
    apellidos = new_contact['apellidos']
    email = new_contact['email']
    telefono = new_contact['telefono']

    cur.execute('UPDATE contactos SET nombre = %s, apellidos = %s, email = %s, telefono = %s WHERE id = %s RETURNING *', (nombre, apellidos, email, telefono, id))
    updated_contact = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if updated_contact is None:
        return jsonify({'message': 'Contact not found'}), 404
    return jsonify(updated_contact)

@app.get('/contacts/<id>')
def get_contact(id):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM contactos WHERE id = %s', (id,))
    contact = cur.fetchone()

    if contact is None:
        return jsonify({'message': 'Contact not found'}), 404
    return jsonify(contact)


if __name__ == '__main__':
    app.run(debug=True)