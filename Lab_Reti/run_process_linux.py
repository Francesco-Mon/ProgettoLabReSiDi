import subprocess
import time

def launch_client(clientid):
    print(f"Lancio del client {clientid}")
    
    subprocess.Popen(["gnome-terminal", "--", "python3", "client_login_automatico.py"])

def main():
    num_clients = 5

    for i in range(num_clients):
        launch_client(i + 1)
        time.sleep(1)

if __name__ == "__main__":
    main()