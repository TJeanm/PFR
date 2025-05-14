import paramiko
import socket
import subprocess


LIDAR_PROGRAMME = "Programmes\\lidar_TCP_Serveur_v2.py"
def execute_ssh_command(command):
    raspberry_ip = "192.168.164.181"
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
lidar_command = "python3 /home/groupe5/lidar/TCP_client.py"
execute_ssh_command(lidar_command)

# Lancer un script Python
subprocess.run(["python", LIDAR_PROGRAMME])
