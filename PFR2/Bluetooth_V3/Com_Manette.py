import pygame
import time
import subprocess
import os

# Def des commandes lente
ARRET = "m"
AVANCE = "z"
RECULE = "s"
DROITE = "d"
GAUCHE = "q"
AVANCE_GAUCHE = "a"
AVANCE_DROITE = "e"
RECULE_GAUCHE = "w"
RECULE_DROITE = "x"
# Def des commandes rapide
AVANCE_RAPIDE = "t"
RECULE_RAPIDE = "g"
GAUCHE_RAPIDE = "f"
DROITE_RAPIDE = "h"
AVANCE_GAUCHE_RAPIDE = "r"
AVANCE_DROITE_RAPIDE = "y"
RECULE_GAUCHE_RAPIDE = "v"
RECULE_DROITE_RAPIDE = "b"

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
        transmissionValue = ""
        value_btn = [0] * joystick.get_numbuttons()
        value_joy = [0] * joystick.get_numaxes()

        for i in range(joystick.get_numbuttons()):
            value_btn[i] = joystick.get_button(i)

        for i in range(joystick.get_numaxes()):
            value = joystick.get_axis(i)
            if value > 0.8:
                value = 1
            elif value < -0.8:
                value = -1
            else:
                value = 0
            value_joy[i] = value

        # Choix de la commande à exécuter (value_btn[10] rend plus rapide)
        if value_btn[10] == 0 :
            if value_joy[1] == 1 :
                if value_joy[2] == 1 :
                    transmission = AVANCE_DROITE
                elif value_joy[2] == -1 :
                    transmission = AVANCE_GAUCHE
                else :
                    transmission = AVANCE

            elif value_joy[1] == -1 :
                if value_joy[2] == 1 :
                    transmission = RECULE_DROITE
                elif value_joy[2] == -1 :
                    transmission = RECULE_GAUCHE
                else :
                    transmission = RECULE
            elif value_joy[2] == 1 :
                transmission = DROITE
            elif value_joy[2] == -1 :
                transmission = GAUCHE
            else :
                transmission = ARRET

        else :
            if value_joy[1] == 1 :
                if value_joy[2] == 1 :
                    transmission = AVANCE_DROITE_RAPIDE
                elif value_joy[2] == -1 :
                    transmission = AVANCE_GAUCHE_RAPIDE
                else :
                    transmission = AVANCE_RAPIDE

            elif value_joy[1] == -1 :
                if value_joy[2] == 1 :
                    transmission = RECULE_DROITE_RAPIDE
                elif value_joy[2] == -1 :
                    transmission = RECULE_GAUCHE_RAPIDE
                else :
                    transmission = RECULE_RAPIDE
            elif value_joy[2] == 1 :
                transmission = DROITE_RAPIDE
            elif value_joy[2] == -1 :
                transmission = GAUCHE_RAPIDE
            else :
                transmission = ARRET


        print(transmission)
        ecrire_commande_fichier(transmission)
        #time.sleep(0.5)  # Tempo pour avoir le temps de lire les infos
        subprocess.run(["python", os.getcwd()+"\\envoie_bluetooth.py"])  # Exécute le script interface_bluetooth.py.py

except KeyboardInterrupt:
    print("🛑 Arrêt du programme")
finally:
    pygame.quit()