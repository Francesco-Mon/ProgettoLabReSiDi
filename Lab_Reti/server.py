from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import mysql.connector
import json
import urllib
import threading
import mysql.connector.errors
import bcrypt
import time
import csv

# Configurazione database
db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'biblioteca'
}

# Lock per garantire l'accesso al database
db_lock = threading.Lock()

# Connessione al database
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

def log_response_time(start_time, end_time, method, path, status_code):
    duration = (end_time - start_time)*1000
    log_message = {
        'method': method,
        'path': path,
        'status': status_code,
        'duration (ms)': f"{duration:.4f}"
    }
    
    with open('response_times.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=log_message.keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(log_message)

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        start_time = time.time()
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)
        status_code = 200

        if path == '/libri':
            self.get_libri()
        elif path.startswith('/libri/'):
            libro_id = int(path.split('/')[-1])
            self.get_libro(libro_id)
        elif path == '/prestiti':
            self.get_user_prestiti()
        else:
            status_code = 404
            self._set_headers(status_code)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

        end_time = time.time()
        log_response_time(start_time, end_time, "GET", path, status_code)

    def do_POST(self):
        start_time = time.time()
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        status_code = 200

        if path == '/libri':
            self.add_libro()
        elif path == '/register':
            self.register_user()
        elif path == '/login':
            self.login_user()
        elif path == '/change_password':
            self.change_password()
        elif path == '/prestiti':
            self.new_prestito()
        elif path == '/restituzioni':
            self.restituisci_libro()
        else:
            status_code = 404
            self._set_headers(status_code)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

        end_time = time.time()
        log_response_time(start_time, end_time, "POST", path, status_code)

    def do_PUT(self):
        start_time = time.time()
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        status_code = 200

        if path.startswith('/libri/'):
            libro_id = int(path.split('/')[-1])
            self.update_libro(libro_id)
        else:
            status_code = 404
            self._set_headers(status_code)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

        end_time = time.time()
        log_response_time(start_time, end_time, "PUT", path, status_code)

    def do_DELETE(self):
        start_time = time.time()
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        status_code = 200

        if path.startswith('/libri/'):
            libro_id = int(path.split('/')[-1])
            self.delete_libro(libro_id)
        else:
            status_code = 404
            self._set_headers(status_code)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

        end_time = time.time()
        log_response_time(start_time, end_time, "DELETE", path, status_code)

    def get_libri(self):
        with db_lock:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM libri")
            libri = cursor.fetchall()
            conn.close()
        
        self._set_headers()
        self.wfile.write(json.dumps(libri).encode('utf-8'))

    def get_libro(self, libro_id):
        with db_lock:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM libri WHERE id_libro = %s", (libro_id,))
            libro = cursor.fetchone()
            conn.close()
        
        if libro:
            self._set_headers()
            self.wfile.write(json.dumps(libro).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Libro non trovato'}).encode('utf-8'))

    def get_disponibilita(self, libro_id):
        with db_lock:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM libri WHERE id_libro = %s", (libro_id,))
            libro = cursor.fetchone()
            conn.close()
        
        if libro:
            self._set_headers()
            self.wfile.write(json.dumps(libro).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Libro non trovato'}).encode('utf-8'))

    def add_libro(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        nuovo_libro = json.loads(post_data)
        
        titolo = nuovo_libro.get('titolo')
        autore = nuovo_libro.get('autore')
        anno = nuovo_libro.get('anno')

        with db_lock:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO libri (titolo, autore, anno) VALUES (%s, %s, %s)",
                        (titolo, autore, anno))
            conn.commit()
            libro_id = cursor.lastrowid
            conn.close()
        
        self._set_headers(201)
        self.wfile.write(json.dumps({'id_libro': libro_id, 'titolo': titolo, 'autore': autore, 'anno': anno}).encode('utf-8'))

    def update_libro(self, libro_id):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        aggiorna_libro = json.loads(post_data)
        
        titolo = aggiorna_libro.get('titolo')
        autore = aggiorna_libro.get('autore')
        anno = aggiorna_libro.get('anno')

        with db_lock:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE libri SET titolo = %s, autore = %s, anno = %s WHERE id_libro = %s",
                        (titolo, autore, anno, libro_id))
            conn.commit()
            conn.close()
        
        self._set_headers()
        self.wfile.write(json.dumps({'id_libro': libro_id, 'titolo': titolo, 'autore': autore, 'anno': anno}).encode('utf-8'))

    def delete_libro(self, libro_id):
        with db_lock:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM libri WHERE id_libro = %s", (libro_id,))
            conn.commit()
            conn.close()
        
        self._set_headers()
        self.wfile.write(json.dumps({'message': 'Libro eliminato'}).encode('utf-8'))

    def new_prestito(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        nuovo_prestito = json.loads(post_data)
        
        id_libro = nuovo_prestito.get('id_libro')
        id_utente = nuovo_prestito.get('id_utente')
        data_prestito = nuovo_prestito.get('data_prestito')

        with db_lock:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Controlla la disponibilità del libro
            cursor.execute("SELECT disponibilita FROM libri WHERE id_libro = %s", (id_libro,))
            result = cursor.fetchone()
            if not result or result[0] != 'YES':
                # Se il libro non è disponibile
                conn.close()
                self._set_headers(400)  # Bad Request
                self.wfile.write(json.dumps({'error': 'Il libro non è disponibile per il prestito.'}).encode('utf-8'))
                return
            
            cursor.execute("INSERT INTO prestiti (id_libro, id_utente, data_prestito) VALUES (%s, %s, %s)",
                        (id_libro, id_utente, data_prestito))
            conn.commit()
            id_prestito = cursor.lastrowid

            cursor.execute("UPDATE libri SET disponibilita = 'NO' WHERE id_libro = %s", (id_libro,))
            conn.commit()

            conn.close()
        
        self._set_headers(201)
        self.wfile.write(json.dumps({'id_prestito': id_prestito, 'id_libro': id_libro, 'id_utente': id_utente, 'data_prestito': data_prestito}).encode('utf-8'))

    def restituisci_libro(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        restituzione = json.loads(post_data)
        
        id_libro = restituzione.get('id_libro')
        id_utente = restituzione.get('id_utente')
        data_restituzione = restituzione.get('data_restituzione')

        with db_lock:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Verifica che esista un prestito attivo per questo libro e utente
            cursor.execute("""
                SELECT id_prestito 
                FROM prestiti 
                WHERE id_libro = %s AND id_utente = %s AND restituito = 'NO'
            """, (id_libro, id_utente))
            result = cursor.fetchone()
            
            if not result:
                # Se non esiste un prestito attivo
                conn.close()
                self._set_headers(400)  # Bad Request
                self.wfile.write(json.dumps({'error': 'Nessun prestito attivo trovato per questo libro e utente.'}).encode('utf-8'))
                return
            
            id_prestito = result[0]

            # Aggiorna la disponibilità del libro
            cursor.execute("UPDATE libri SET disponibilita = 'YES' WHERE id_libro = %s", (id_libro,))
            conn.commit()

            # Aggiorna lo stato del prestito
            cursor.execute("""
                UPDATE prestiti 
                SET restituito = 'YES', data_restituzione = %s 
                WHERE id_prestito = %s
            """, (data_restituzione, id_prestito))
            conn.commit()

            conn.close()
        
        self._set_headers(200)
        self.wfile.write(json.dumps({'id_prestito': id_prestito, 'id_libro': id_libro, 'id_utente': id_utente, 'data_restituzione': data_restituzione}).encode('utf-8'))

    def get_user_prestiti(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)
        id_utente = query.get('id_utente')

        if id_utente:
            id_utente = id_utente[0]

            with db_lock:
                conn = get_db_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT id_prestito, id_libro, id_utente, 
                    DATE_FORMAT(data_prestito, '%Y-%m-%d') as data_prestito, 
                    DATE_FORMAT(data_restituzione, '%Y-%m-%d') as data_restituzione
                    FROM prestiti 
                    WHERE id_utente = %s
                """, (id_utente,))
                prestiti = cursor.fetchall()
                conn.close()

            self._set_headers()
            self.wfile.write(json.dumps(prestiti).encode('utf-8'))
        else:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'Parametro id_utente mancante'}).encode('utf-8'))


    def register_user(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        nuovo_utente = json.loads(post_data)

        nome = nuovo_utente.get('nome')
        cognome = nuovo_utente.get('cognome')
        username = nuovo_utente.get('username')
        password = nuovo_utente.get('password')
        ruolo = nuovo_utente.get('ruolo', 'Cliente')  # Impostiamo il ruolo predefinito a "Cliente"

        # Hashing della password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        with db_lock:
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Recupero dell'id del ruolo
                cursor.execute("SELECT id_ruolo FROM ruoli WHERE descrizione = %s", (ruolo,))
                ruolo_record = cursor.fetchone()

                if ruolo_record:
                    id_ruolo = ruolo_record[0]
                    cursor.execute("INSERT INTO utenti (nome, cognome, username, password, id_ruolo) VALUES (%s, %s, %s, %s, %s)",
                                (nome, cognome, username, hashed_password, id_ruolo))
                    conn.commit()
                    utente_id = cursor.lastrowid
                    conn.close()
                    self._set_headers(201)
                    self.wfile.write(json.dumps({'id_utente': utente_id, 'nome': nome, 'cognome': cognome, 'username': username, 'ruolo': ruolo}).encode('utf-8'))
                else:
                    conn.close()
                    self._set_headers(400)
                    self.wfile.write(json.dumps({'error': 'Ruolo non valido'}).encode('utf-8'))
            except mysql.connector.errors.IntegrityError as e:
                conn.close()
                if e.errno == 1062:
                    self._set_headers(409)
                    self.wfile.write(json.dumps({'error': 'Username già utilizzato'}).encode('utf-8'))
                else:
                    self._set_headers(500)
                    self.wfile.write(json.dumps({'error': 'Errore del server'}).encode('utf-8'))

    def login_user(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        dati_login = json.loads(post_data)

        username = dati_login.get('username')
        password = dati_login.get('password')

        with db_lock:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT utenti.id_utente, utenti.password, ruoli.descrizione AS ruolo FROM utenti INNER JOIN ruoli ON utenti.id_ruolo = ruoli.id_ruolo WHERE utenti.username = %s", (username,))
            utente = cursor.fetchone()
            conn.close()

        if utente:
            stored_password = utente['password'].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                self._set_headers()
                self.wfile.write(json.dumps({'id_utente': utente['id_utente'], 'username': username, 'ruolo': utente['ruolo']}).encode('utf-8'))
            else:
                self._set_headers(401)
                self.wfile.write(json.dumps({'error': 'Credenziali non valide'}).encode('utf-8'))
        else:
            self._set_headers(401)
            self.wfile.write(json.dumps({'error': 'Credenziali non valide'}).encode('utf-8'))

    def change_password(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        dati_password = json.loads(post_data)

        username = dati_password.get('username')
        old_password = dati_password.get('old_password')
        new_password = dati_password.get('new_password')

        with db_lock:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT password FROM utenti WHERE username = %s", (username,))
            utente = cursor.fetchone()

            if utente:
                stored_password = utente['password'].encode('utf-8')
                if bcrypt.checkpw(old_password.encode('utf-8'), stored_password):
                    hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute("UPDATE utenti SET password = %s WHERE username = %s", (hashed_new_password, username))
                    conn.commit()
                    conn.close()
                    self._set_headers()
                    self.wfile.write(json.dumps({'message': 'Password modificata con successo'}).encode('utf-8'))
                else:
                    conn.close()
                    self._set_headers(401)
                    self.wfile.write(json.dumps({'error': 'Vecchia password errata'}).encode('utf-8'))
            else:
                conn.close()
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Utente non trovato'}).encode('utf-8'))

class ThreadingSimpleServer(socketserver.ThreadingMixIn, HTTPServer):
    pass

# Funzione per avviare il server con il supporto per il multithreading
def run(server_class=ThreadingSimpleServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server in esecuzione sulla porta {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
