import paramiko
import socket
import subprocess
import os

def get_local_ip():
    hostname = socket.gethostname()  # Récupère le nom de l'hôte de la machine
    local_ip = socket.gethostbyname(hostname)  # Récupère l'IP associée au nom d'hôte
    return local_ip

def execute_ssh_command(command):
    raspberry_ip = "192.168.94.181"
    username = "groupe5"
    password = "1234"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(raspberry_ip, username=username, password=password)
        print("Connexion SSH réussie.")
        ssh.exec_command(command)
        print("Commande SSH exécutée : ", command)
    except Exception as e:
        print(f"Erreur SSH : {e}")
    finally:
        pass

# 2. Ensuite, lancer la commande SSH (pendant que les données arrivent)
local_ip = get_local_ip()
commande_camera = (
    f"nohup bash -c \"libcamera-vid -t 0 --width 320 --height 240 "
    f"--framerate 15 --codec h264 -o - | ffmpeg -f h264 -i - "
    f"-f mpegts udp://{local_ip}:1234?pkt_size=1316\" > /dev/null 2>&1 &"
)
execute_ssh_command(commande_camera)


# Chemin vers VLC si nécessaire (modifie si besoin)
vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"

# Flux UDP
stream_url = "udp://@:1234"

try:
    subprocess.Popen([vlc_path, stream_url])
    print("VLC lancé avec succès.")
except FileNotFoundError:
    print("Erreur : VLC n'est pas trouvé. Vérifie le chemin.")
except Exception as e:
    print("Erreur lors du lancement de VLC :", e)