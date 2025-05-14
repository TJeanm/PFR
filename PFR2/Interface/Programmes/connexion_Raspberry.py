import paramiko

#def start_lidar_program():
raspberry_ip = "192.168.164.181"  # IP de la Raspberry Pi
username = "groupe5"  # Nom d'utilisateur par défaut de la Raspberry Pi
password = "1234"  # Mot de passe par défaut de la Raspberry Pi

# Créer un client SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Ajouter automatiquement les clés non vérifiées

try:
    # Connexion SSH à la Raspberry Pi
    ssh.connect(raspberry_ip, username=username, password=password)
    print("Connexion SSH réussie.")

    # Lancer le programme du Lidar
    stdin, stdout, stderr = ssh.exec_command("python3 /home/groupe5/lidar/TCP_client.py")
    print("Programme Lidar lancé.")

    # Optionnel : Récupérer la sortie du programme
    output = stdout.read().decode()
    print("Sortie du programme : ", output)
except Exception as e:
    print(f"Erreur SSH : {e}")
finally:
    ssh.close()