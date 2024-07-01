import csv

# Inizializza variabili
post_durations = []

# Leggi il file
with open('response_times_3500client.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['method'] == 'POST':
            post_durations.append(float(row['duration (ms)']))

# Calcola la media
if post_durations:
    average_duration = sum(post_durations) / len(post_durations)
    print(f"La media dei tempi di risposta delle richieste POST è: {average_duration} ms")
else:
    print("Non ci sono richieste POST nel file.")
