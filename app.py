from flask import Flask
from psycopg2 import connect

app = Flask(__name__)

host = 'localhost'
port = 5432
dbname = 'postgres'
user = 'jesusraulrg'
password = 'DSitMoM.12'


def get_connection():
    conn = connect(host=host, port=port, dbname=dbname, user=user, password=password)
    return conn

@app.route('/')
def home():
    conn = get_connection()
    cur = conn.cursor()
    
    result = cur.execute('SELECT 1 + 1')
    print(result)

    return 'Hello World'

@app.get('/contacts')
def get_contacts():
    return 'getting contacts'

@app.post('/contacts')
def create_contact():
    return 'creatting contact'

@app.delete('/contacts')
def delete_contact():
    return 'deleting contact'

@app.put('/contacts')
def upgrade_contact():
    return 'updating contact'






if __name__ == '__main__':
    app.run(debug=True)