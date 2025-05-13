import subprocess
import time
import keyboard
import asyncio
import csv
from communication_HM10 import communication

CHEMIN_POSITION = "Casse_Noisette/resultats_detection.csv"
ACTIVATION_DETECTION = "Programmes\\detection_une_couleur.py"

POS_MIN = 0
POS_X_MAX = 4032
POS_Y_MAX = 3024

def lire_position():
    try:
        with open(CHEMIN_POSITION, "r", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                x = int(row["X"])
                y = int(row["Y"])
                return x, y
    except Exception as e:
        print(f"Erreur de lecture : {e}")
        return 0, 0  # Valeurs par défaut en cas d'erreur

def reaction_robot(x, y):
    if (x == 0 and y == 0) or (x == POS_X_MAX and y == POS_Y_MAX):
        return "d"
    elif x <= POS_X_MAX / 3:
        return "q"
    elif x >= POS_X_MAX * 2 / 3:
        return "d"
    else:
        return "z"

async def main():
    print("Appuyez sur 'l' pour arrêter...")

    #com = communication()
    #await com.init_HM10()
    ancien_temp = 0
    while True:
        if keyboard.is_pressed('l'):
            #await com.envoie_bluetooth("m")
            break

        new_temp = time.time()
        if new_temp - ancien_temp >= 0.5:
            subprocess.run(["python", ACTIVATION_DETECTION])
            x, y = lire_position()
            print(f"x = {x} et y = {y}")
            envoie = reaction_robot(x, y)
            #await com.envoie_bluetooth(envoie)

            ancien_temp = new_temp

        time.sleep(0.02)  # Pour ne pas surcharger le CPU

    print("Fin du programme.")

if __name__ == "__main__":
    asyncio.run(main())
