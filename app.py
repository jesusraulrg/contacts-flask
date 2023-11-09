from flask import Flask, jsonify, request
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
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT 1 + 1')
    result = cur.fetchone()
    
    print(result)

    return 'Hello World'

@app.get('/contacts')
def get_contacts():
    return 'getting contacts'

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

@app.delete('/contacts')
def delete_contact():
    return 'deleting contact'

@app.put('/contacts')
def update_contact():
    return 'updating contact'

@app.get('/contacts')
def get_contact():
    return 'getting contact'




if __name__ == '__main__':
    app.run(debug=True)