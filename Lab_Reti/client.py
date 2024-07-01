import requests
from datetime import datetime
import os
import getpass

# URL del server
base_url = 'http://127.0.0.1:8080'

# Variabili di stato per il login e il ruolo
logged_in = False
user_role = None
user_id = None

# Funzioni per la gestione della biblioteca
def get_libri():
    response = requests.get(f"{base_url}/libri")
    if response.status_code == 200:
        libri = response.json()
        print("Libri presenti nella biblioteca:")
        for libro in libri:
            disponibilita = 'SI' if libro['disponibilita'] == 'YES' else 'NO'
            print(f"ID: {libro['id_libro']}, Titolo: {libro['titolo']}, Autore: {libro['autore']}, Anno: {libro['anno']}, Disponibilità: {disponibilita}")
    else:
        print("Errore nella richiesta GET")

def get_libro(libro_id):
    response = requests.get(f"{base_url}/libri/{libro_id}")
    if response.status_code == 200:
        libro = response.json()
        disponibilita = 'SI' if libro['disponibilita'] == 'YES' else 'NO'
        print(f"ID: {libro['id_libro']}, Titolo: {libro['titolo']}, Autore: {libro['autore']}, Anno: {libro['anno']}, Disponibilità: {disponibilita}")
    else:
        print("Errore nella richiesta GET")

def add_libro(titolo, autore, anno):
    if user_role != 'Amministratore':
        print("\n-----------------------------------------------------------------")
        print("Accesso negato: solo gli amministratori possono aggiungere libri.")
        print("-----------------------------------------------------------------")
        return
    nuovo_libro = {'titolo': titolo, 'autore': autore, 'anno': anno}
    response = requests.post(f"{base_url}/libri", json=nuovo_libro)
    if response.status_code == 201:
        libro = response.json()
        print("\n----------------------------")
        print("Libro aggiunto con successo:")
        print("----------------------------")
        print(f"ID: {libro['id_libro']}, Titolo: {libro['titolo']}, Autore: {libro['autore']}, Anno: {libro['anno']}")
    else:
        print("Errore nella richiesta POST")

def update_libro(libro_id, titolo, autore, anno):
    if user_role != 'Amministratore':
        print("\n-----------------------------------------------------------------")
        print("Accesso negato: solo gli amministratori possono aggiornare libri.")
        print("-----------------------------------------------------------------")
        return
    aggiorna_libro = {'titolo': titolo, 'autore': autore, 'anno': anno}
    response = requests.put(f"{base_url}/libri/{libro_id}", json=aggiorna_libro)
    if response.status_code == 200:
        libro = response.json()
        print("\n------------------------------")
        print("Libro aggiornato con successo:")
        print("------------------------------")
        print(f"ID: {libro['id_libro']}, Titolo: {libro['titolo']}, Autore: {libro['autore']}, Anno: {libro['anno']}")
    else:
        print("Errore nella richiesta PUT")

def delete_libro(libro_id):
    if user_role != 'Amministratore':
        print("\n----------------------------------------------------------------")
        print("Accesso negato: solo gli amministratori possono eliminare libri.")
        print("----------------------------------------------------------------")
        return
    response = requests.delete(f"{base_url}/libri/{libro_id}")
    if response.status_code == 200:
        print("\n----------------------------")
        print("Libro eliminato con successo")
        print("----------------------------")
    else:
        print("Errore nella richiesta DELETE")

def new_prestito(libro_id):
    disponibile = get_disponibilita(libro_id)
    if disponibile:
        data_prestito = datetime.now().strftime('%Y-%m-%d')
        nuovo_prestito = {'id_utente': user_id, 'id_libro': libro_id, 'data_prestito': data_prestito}
        response = requests.post(f"{base_url}/prestiti", json=nuovo_prestito)
        if response.status_code == 201:
            print("\n----------------------------------------------------------------------------------")
            print("Prestito registrato con successo:")
            print(f"ID Utente: {user_id}, ID Libro: {libro_id}, Data Prestito: {data_prestito}")
            print("----------------------------------------------------------------------------------")
        else:
            print("Errore nella richiesta di prestito")
    else:
        print("\n------------------------------------")
        print("Il libro richiesto non è disponibile")
        print("------------------------------------")

def restituisci_libro(libro_id):
    data_restituzione = datetime.now().strftime('%Y-%m-%d')
    restituzione = {'id_utente': user_id, 'id_libro': libro_id, 'data_restituzione': data_restituzione}
    response = requests.post(f"{base_url}/restituzioni", json=restituzione)
    
    if response.status_code == 200:
        print("\n----------------------------------------------------------------------------------")
        print("Restituzione registrata con successo:")
        print(f"ID Utente: {user_id}, ID Libro: {libro_id}, Data Restituzione: {data_restituzione}")
        print("----------------------------------------------------------------------------------")
    else:
        print("Errore nella richiesta di restituzione")

def get_disponibilita(libro_id):
    response = requests.get(f"{base_url}/libri/{libro_id}")
    if response.status_code == 200:
        libro = response.json()
    is_disponibile = 1 if libro['disponibilita'] == 'YES' else 0
    return is_disponibile

def get_user_prestiti(user_id):
    response = requests.get(f"{base_url}/prestiti?id_utente={user_id}")
    if response.status_code == 200:
        prestiti = response.json()
        print("Prestiti dell'utente:")
        for prestito in prestiti:
            print(f"ID Prestito: {prestito['id_prestito']}, ID Libro: {prestito['id_libro']}, Data Prestito: {prestito['data_prestito']}, Data Restituzione: {prestito['data_restituzione']}")
    else:
        print("Errore nella richiesta GET")
    
# Funzioni per la gestione dell'autenticazione
def login(username, password):
    global logged_in, user_role, user_id
    response = requests.post(f"{base_url}/login", json={'username': username, 'password': password})
    if response.status_code == 200:
        data = response.json()
        logged_in = True
        user_role = data.get('ruolo', 'utente')
        user_id = data.get('id_utente')
        print("\n-----------------------------")
        print("Login effettuato con successo")
        print(f"Ruolo dell'utente: {user_role}")
        print("-----------------------------")
    else:
        print("Errore nel login: credenziali non valide")

def register(username, password, confirm_password, pin):
    global logged_in, user_role, user_id
    if password != confirm_password:
        print("Errore: le password non coincidono")
        return
    # Verifica del pin per il ruolo di amministratore
    ruolo = 'utente'
    if pin == '0000':
        ruolo = 'Amministratore'
    try:
        response = requests.post(f"{base_url}/register", json={'username': username, 'password': password, 'ruolo': ruolo, 'nome': nome, 'cognome': cognome})
        response.raise_for_status()
        if response.status_code == 201:
            data = response.json()
            logged_in = True
            user_role = data.get('ruolo', ruolo)
            user_id = data.get('id_utente')
            print("\n--------------------------------------------------------")
            print("Registrazione effettuata con successo e login automatico")
            print(f"Ruolo dell'utente: {user_role}")
            print("--------------------------------------------------------")
        else:
            print("Errore nella registrazione")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 409:
            print("Errore: Username già utilizzato")
        else:
            print(f"Errore HTTP {e.response.status_code}: {e.response.text}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Errore di connessione: {errc}")
    except requests.exceptions.RequestException as err:
        print(f"Errore durante la richiesta: {err}")

def change_password(username, old_password, new_password, confirm_new_password):
    if new_password != confirm_new_password:
        print("Errore: le nuove password non coincidono")
        return
    response = requests.post(f"{base_url}/change_password", json={'username': username, 'old_password': old_password, 'new_password': new_password})
    if response.status_code == 200:
        print("\n--------------------------------")
        print("Password modificata con successo")
        print("--------------------------------")
    elif response.status_code == 404:
        print("Errore: Utente non trovato")
    elif response.status_code == 400:
        print("Errore: La vecchia password non è corretta")
    else:
        print("Errore nella modifica della password")

# Funzione per pulire lo schermo
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    while True:
        if not logged_in:
            print("\nOperazioni di autenticazione disponibili:")
            print("1. Accedi")
            print("2. Registrati")
            print("3. Modifica la password")
            print("4. Esci")

            scelta = input("Scegli un'opzione: ")

            if scelta == '1':
                username = input("Inserisci il nome utente: ")
                password = getpass.getpass("Inserisci la password: ")
                clear_screen()
                login(username, password)
            elif scelta == '2':
                nome = input("Inserisci il tuo nome: ")
                cognome = input("Inserisci il tuo cognome: ")
                username = input("Inserisci il nome utente: ")
                password = getpass.getpass("Inserisci la password: ")
                confirm_password = getpass.getpass("Conferma la password: ")
                pin = input("Inserisci il pin per il ruolo di amministratore (lascia vuoto se utente): ")
                clear_screen()
                register(username, password, confirm_password, pin)
            elif scelta == '3':
                username = input("Inserisci il nome utente: ")
                old_password = getpass.getpass("Inserisci la vecchia password: ")
                new_password = getpass.getpass("Inserisci la nuova password: ")
                confirm_new_password = getpass.getpass("Conferma la nuova password: ")
                clear_screen()
                change_password(username, old_password, new_password, confirm_new_password)
            elif scelta == '4':
                clear_screen()
                print("Uscita dal programma.")
                break
            else:
                clear_screen()
                print("Scelta non valida. Riprova.")
        else:
            print("\nOperazioni disponibili:")
            print("1. Visualizza tutti i libri")
            print("2. Visualizza un libro")
            print("3. Aggiungi un nuovo libro (solo amministratori)")
            print("4. Aggiorna un libro esistente (solo amministratori)")
            print("5. Elimina un libro (solo amministratori)")
            print("6. Registra un nuovo prestito")
            print("7. Restituisci un libro")
            print("8. Visualizza i tuoi prestiti")
            print("9. Esci")

            scelta = input("Scegli un'opzione: ")

            if scelta == '1':
                clear_screen()
                get_libri()
            elif scelta == '2':
                clear_screen()
                libro_id = input("Inserisci l'ID del libro: ")
                get_libro(libro_id)
            elif scelta == '3':
                clear_screen()
                if user_role == 'Amministratore':
                    titolo = input("Inserisci il titolo del libro: ")
                    autore = input("Inserisci l'autore del libro: ")
                    anno = input("Inserisci l'anno del libro: ")
                    add_libro(titolo, autore, anno)
                else:
                    print("\n-----------------------------------------------------------------")
                    print("Accesso negato: solo gli amministratori possono aggiungere libri.")
                    print("-----------------------------------------------------------------")
            elif scelta == '4':
                clear_screen()
                if user_role == 'Amministratore':
                    libro_id = input("Inserisci l'ID del libro: ")
                    titolo = input("Inserisci il nuovo titolo del libro: ")
                    autore = input("Inserisci il nuovo autore del libro: ")
                    anno = input("Inserisci il nuovo anno del libro: ")
                    update_libro(libro_id, titolo, autore, anno)
                else:
                    print("\n-----------------------------------------------------------------")
                    print("Accesso negato: solo gli amministratori possono aggiornare libri.")
                    print("-----------------------------------------------------------------")
            elif scelta == '5':
                clear_screen()
                if user_role == 'Amministratore':
                    libro_id = input("Inserisci l'ID del libro da eliminare: ")
                    delete_libro(libro_id)
                else:
                    print("\n----------------------------------------------------------------")
                    print("Accesso negato: solo gli amministratori possono eliminare libri.")
                    print("----------------------------------------------------------------")
            elif scelta == '6':
                clear_screen()
                libro_id = input("Inserisci l'ID del libro da prendere in prestito: ")
                new_prestito(libro_id)
            elif scelta == '7':
                clear_screen()
                libro_id = input("Inserisci l'ID del libro da restituire: ")
                restituisci_libro(libro_id)
            elif scelta == '8':
                clear_screen()
                get_user_prestiti(user_id)
            elif scelta == '9':
                clear_screen()
                print("Uscita dal programma.")
                break
            else:
                clear_screen()
                print("Scelta non valida. Riprova.")
