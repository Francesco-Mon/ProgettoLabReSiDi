import mysql.connector

# Configurazione del database
db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1'
}

# Creazione della connessione al database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Creazione del database
cursor.execute("CREATE DATABASE IF NOT EXISTS biblioteca")
cursor.execute("USE biblioteca")

# Creazione della tabella libri
cursor.execute("""
    CREATE TABLE IF NOT EXISTS libri (
        id_libro INT AUTO_INCREMENT PRIMARY KEY,
        titolo VARCHAR(255) NOT NULL,
        autore VARCHAR(255) NOT NULL,
        anno INT NOT NULL,
        disponibilita CHAR(3) DEFAULT 'YES'
    )
""")

# Creazione della tabella ruoli
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ruoli (
        id_ruolo INT AUTO_INCREMENT PRIMARY KEY,
        descrizione VARCHAR(255) NOT NULL
    )
""")

# Creazione della tabella utenti
cursor.execute("""
    CREATE TABLE IF NOT EXISTS utenti (
        id_utente INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        cognome VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        id_ruolo INT NOT NULL,
        FOREIGN KEY (id_ruolo) REFERENCES ruoli(id_ruolo)
    )
""")

# Creazione della tabella prestiti
cursor.execute("""
    CREATE TABLE IF NOT EXISTS prestiti (
        id_prestito INT AUTO_INCREMENT PRIMARY KEY,
        id_libro INT NOT NULL,
        id_utente INT NOT NULL,
        data_prestito DATE NOT NULL,
        data_restituzione DATE DEFAULT NULL,
        restituito CHAR(3) DEFAULT 'NO',
        FOREIGN KEY (id_libro) REFERENCES libri(id_libro),
        FOREIGN KEY (id_utente) REFERENCES utenti(id_utente)
    )
""")

# Inserimento dei dati di esempio per la tabella ruoli
ruoli = [
    ('Amministratore'),
    ('Utente')
]

# Inserimento dei dati di esempio per la tabella libri
libri = [
    ('Il nome della rosa', 'Umberto Eco', 1980),
    ('1984', 'George Orwell', 1949),
    ('Il piccolo principe', 'Antoine de Saint-Exupéry', 1943),
    ('La Divina Commedia', 'Dante Alighieri', 1320),
    ('Orgoglio e pregiudizio', 'Jane Austen', 1813),
    ('Moby Dick', 'Herman Melville', 1851),
    ('Guerra e pace', 'Lev Tolstoj', 1869),
    ('Il grande Gatsby', 'F. Scott Fitzgerald', 1925),
    ('Don Chisciotte', 'Miguel de Cervantes', 1605),
    ('Cime tempestose', 'Emily Brontë', 1847),
    ('Anna Karenina', 'Lev Tolstoj', 1877),
    ('Madame Bovary', 'Gustave Flaubert', 1857),
    ('Le avventure di Alice nel Paese delle Meraviglie', 'Lewis Carroll', 1865),
    ('Cent\'anni di solitudine', 'Gabriel García Márquez', 1967),
    ('Cronache del ghiaccio e del fuoco', 'George R.R. Martin', 1996),
    ('Il Signore degli Anelli', 'J.R.R. Tolkien', 1954),
    ('Il giovane Holden', 'J.D. Salinger', 1951),
    ('La metamorfosi', 'Franz Kafka', 1915),
    ('Il vecchio e il mare', 'Ernest Hemingway', 1952),
    ('Il cacciatore di aquiloni', 'Khaled Hosseini', 2003),
    ('La fattoria degli animali', 'George Orwell', 1945),
    ('Il fu Mattia Pascal', 'Luigi Pirandello', 1904),
    ('Piccole donne', 'Louisa May Alcott', 1868),
    ('Il processo', 'Franz Kafka', 1925),
    ('Il sole sorge ancora', 'Ernest Hemingway', 1926),
    ('Il ritratto di Dorian Gray', 'Oscar Wilde', 1890),
    ('La storia infinita', 'Michael Ende', 1979),
    ('L\'idiota', 'Fedor Dostoevskij', 1869),
    ('Il giardino segreto', 'Frances Hodgson Burnett', 1911),
    ('Il deserto dei Tartari', 'Dino Buzzati', 1940),
    ('Il giro di vite', 'Henry James', 1898),
    ('Gli anni', 'Virginia Woolf', 1937),
    ('I miserabili', 'Victor Hugo', 1862),
    ('Lo straniero', 'Albert Camus', 1942),
    ('Mille splendidi soli', 'Khaled Hosseini', 2007),
    ('Matilde', 'Roald Dahl', 1988),
    ('Il castello', 'Franz Kafka', 1926),
    ('Il barone rampante', 'Italo Calvino', 1957),
    ('La storia', 'Elsa Morante', 1974),
    ('Il buio oltre la siepe', 'Harper Lee', 1960),
    ('Uno, nessuno e centomila', 'Luigi Pirandello', 1926),
    ('La coscienza di Zeno', 'Italo Svevo', 1923),
    ('Il piccolo Lord', 'Frances Hodgson Burnett', 1886),
    ('Il sentiero dei nidi di ragno', 'Italo Calvino', 1947),
    ('Il Gattopardo', 'Giuseppe Tomasi di Lampedusa', 1958),
    ('La ragazza di Bube', 'Carlo Cassola', 1960),
    ('Il visconte dimezzato', 'Italo Calvino', 1952),
    ('Il vecchio e il bambino', 'Luigi Pirandello', 1926),
    ('I racconti di Canterbury', 'Geoffrey Chaucer', 1400)
]

# Inserimento dei dati nella tabella ruoli
cursor.executemany("INSERT INTO ruoli (descrizione) VALUES (%s)", [(ruolo,) for ruolo in ruoli])

# Inserimento dei libri nella tabella
cursor.executemany("INSERT INTO libri (titolo, autore, anno) VALUES (%s, %s, %s)", libri)

# Conferma delle operazioni
conn.commit()

# Chiusura della connessione
cursor.close()
conn.close()

print("Database e tabella creati con successo, dati di esempio inseriti.")
