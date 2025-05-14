import asyncio
import sys
import pygame
from bleak import BleakClient, BleakScanner
import keyboard
from communication_HM10 import communication

UART_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
TARGET_NAME = "robot2"
SCAN_TIMEOUT = 5.0  # secondes

# Les commandes
ARRET = "m"
AVANCE = "z"
RECULE = "s"
DROITE = "d"
GAUCHE = "q"
AVANCE_GAUCHE = "a"
AVANCE_DROITE = "e"
RECULE_GAUCHE = "w"
RECULE_DROITE = "x"
# Commandes rapides
AVANCE_RAPIDE = "t"
RECULE_RAPIDE = "g"
GAUCHE_RAPIDE = "f"
DROITE_RAPIDE = "h"
AVANCE_GAUCHE_RAPIDE = "r"
AVANCE_DROITE_RAPIDE = "y"
RECULE_GAUCHE_RAPIDE = "v"
RECULE_DROITE_RAPIDE = "b"
MODE_MANUEL = "p"
MODE_AUTO = "o"
MODE_VOC = "i"

# seuil de deadzone : tout |axe| < 0.2 est considéré 0
DEADZONE = 0.2
# délai de boucle ramené à 20 ms
LOOP_DELAY = 0.02
#Fichier activation capteur_ultrason
FICHIER_MDP = "Casse_Noisette/activation_capteur_ultrason.txt"

async def main():
    com = communication()
    await com.init_HM10()
    with open(FICHIER_MDP, "r") as f:
        activation_ultrason = f.read().strip()
    MODE_MANUEL = activation_ultrason
    await com.envoie_bluetooth(MODE_MANUEL)

    # 3) Init pygame + manette
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("🚨 Pas de manette détectée.")
        return
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print(f"🎮 Manette : {joy.get_name()}")

    # 4) boucle lecture/envoi
    last_cmd = None
    try:
        while True:
            # on pompe les events
            pygame.event.pump()

            # lecture boutons
            btn = [joy.get_button(i) for i in range(joy.get_numbuttons())]
            # lecture axes avec deadzone
            axes = []
            for i in range(joy.get_numaxes()):
                v = joy.get_axis(i)
                if abs(v) < DEADZONE:
                    axes.append(0)
                else:
                    axes.append(1 if v > 0 else -1)

            # logique de choix de cmd
            if btn[2] == 1:
                cmd = MODE_AUTO
            elif btn[1] == 1:
                cmd = MODE_MANUEL
            elif btn[3] == 1:
                cmd = MODE_VOC
            elif btn[10] == 0:
                if axes[1] == -1:
                    cmd = (AVANCE_DROITE if axes[2] == 1 else
                           AVANCE_GAUCHE if axes[2] == -1 else
                           AVANCE)
                elif axes[1] == 1:
                    cmd = (RECULE_DROITE if axes[2] == 1 else
                           RECULE_GAUCHE if axes[2] == -1 else
                           RECULE)
                elif axes[2] == 1:
                    cmd = DROITE
                elif axes[2] == -1:
                    cmd = GAUCHE
                else:
                    cmd = ARRET
            else:
                if axes[1] == -1:
                    cmd = (AVANCE_DROITE_RAPIDE if axes[2] == 1 else
                           AVANCE_GAUCHE_RAPIDE if axes[2] == -1 else
                           AVANCE_RAPIDE)
                elif axes[1] == 1:
                    cmd = (RECULE_DROITE_RAPIDE if axes[2] == 1 else
                           RECULE_GAUCHE_RAPIDE if axes[2] == -1 else
                           RECULE_RAPIDE)
                elif axes[2] == 1:
                    cmd = DROITE_RAPIDE
                elif axes[2] == -1:
                    cmd = GAUCHE_RAPIDE
                else:
                    cmd = ARRET

            # 5) envoi si changement + \n pour l'Arduino
            if cmd != last_cmd:
                await com.envoie_bluetooth(cmd)
                last_cmd = cmd

            if (keyboard.is_pressed('l') or btn[0] == 1):  # or btn(0)) :
                pygame.quit()
                await com.close()
                break

    except (keyboard.is_pressed('l') or btn[0] == 1):
        print("\n🛑 Arrêt demandé par l'utilisateur.")
        pygame.quit()
    finally:
        pygame.quit()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
