import pygame
import time
import subprocess
import os

def ecrire_commande_fichier(commande):
    with open("Com_to_Manette.txt", "w", encoding="utf-8") as fichier:
        fichier.write(commande + "\n")

# Initialisation de pygame pour la gestion de la manette
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"🎮 Manette détectée : {joystick.get_name()}")
else:
    print("⚠️ Aucune manette détectée")
    exit()

# Boucle principale pour lire les entrées de la manette
try:
    while True:
        pygame.event.pump()
        transmission = ""
        for i in range(joystick.get_numbuttons()):
            if (i == 0 or i == 10):
                transmission = transmission + f"{joystick.get_button(i)}\n"
        
        for i in range(joystick.get_numaxes()):
            value = joystick.get_axis(i)
            if value > 0.8:
                value = 1
            elif value < -0.8:
                value = -1
            else :
                value = 0
            
            if (i >= 0 and i <= 3):
                transmission = transmission + f"{value}\n"
        
        print(transmission)
        ecrire_commande_fichier(transmission)
        #time.sleep(0.5)  # Tempo pour avoir le temps de lire les infos
        subprocess.run(["python", os.getcwd()+"\\bt_arduino.py"])  # Exécute le script interface_bluetooth.py.py

except KeyboardInterrupt:
    print("🛑 Arrêt du programme")
finally:
    pygame.quit()