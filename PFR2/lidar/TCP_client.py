import socket
import pickle
from rplidar import RPLidar

IP_PC = '192.168.164.151'  # L'adresse IP de l'ordinateur
PORT = 9999  # Le même port que sur le serveur

MAX_TCP_SIZE = 65507  # Taille maximale pour un paquet TCP

# Créer un socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se connecter à l'ordinateur
sock.connect((IP_PC, PORT))

# Connexion avec le Lidar
lidar = RPLidar('/dev/ttyUSB0', timeout=3)
print("Lidar démarré. Envoi des scans...")

try:
    for scan in lidar.iter_scans(max_buf_meas=400):
        try:
            data = pickle.dumps(scan)  # Sérialiser les données du scan
            size = len(data)
            print(f"size = {size}")
            if len(data) > MAX_TCP_SIZE:
                print("⚠️ Paquet trop gros, ignoré.")
                continue  # Ignorer les scans trop gros pour TCP

            sock.sendall(size.to_bytes(4, byteorder='big'))

            # Envoyer les données
            sock.sendall(data)

        except Exception as e:
            print("Erreur d'envoi :", e)

except Exception as e:
    print("Erreur de connexion ou de lecture du Lidar :", e)

finally:
    print("Fermeture...")
    lidar.stop()
    lidar.disconnect()
    sock.close()  # Fermer la connexion TCP
