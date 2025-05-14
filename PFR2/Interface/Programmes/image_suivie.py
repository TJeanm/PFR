import subprocess
import time
import keyboard
import asyncio
import csv
from communication_HM10 import communication

CHEMIN_POSITION = "Casse_Noisette/detection_all.csv"
CHEMIN_IMAGE_A_LIRE = "Casse_Noisette/image_a_lire.txt"
ACTIVATION_DETECTION = "Programmes\\detection_all_simu.py"

image_path = [
    'Casse_Noisette/photo_simu_suivie_reel/1_vide.jpg',
    'Casse_Noisette/photo_simu_suivie_reel/2_gauche.jpg',
    'Casse_Noisette/photo_simu_suivie_reel/3_centre_loin.jpg',
    'Casse_Noisette/photo_simu_suivie_reel/4_centre_proche.jpg',
    'Casse_Noisette/photo_simu_suivie_reel/5_droite_tres_proche.jpg',
    'Casse_Noisette/photo_simu_suivie_reel/6_centre_tres_proche.jpg'
]

POS_MIN = 0
POS_X_MAX = 4032
POS_Y_MAX = 3024

def lire_position():
    try:
        with open(CHEMIN_POSITION, "r", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Forme"].strip().lower() == "cercle" and row["Couleur"].strip().lower() == "rose":
                    x = int(row["X"])
                    y = int(row["Y"])
                    return x, y
        print("Aucun cercle rose trouve.")
        return 0, 0
    except Exception as e:
        print(f"Erreur de lecture : {e}")
        return 0, 0

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
    i = 0
    ancien_temp = 0
    while True:
        if keyboard.is_pressed('l'):
            #await com.envoie_bluetooth("m")
            #await com.close()
            break
        
        new_temp = time.time()
        if new_temp - ancien_temp >= 0.5:
            print("i = ",i)
            with open(CHEMIN_IMAGE_A_LIRE, "w") as f:
                f.write(image_path[i])
            subprocess.run(["python", ACTIVATION_DETECTION])
            x, y = lire_position()
            print(f"x = {x} et y = {y}")
            envoie = reaction_robot(x, y)
            print("Commande envoyé :", envoie)
            #await com.envoie_bluetooth(envoie)
            i+=1
            if i>5 :
                i = 0
            ancien_temp = new_temp

        time.sleep(0.02)  # Pour ne pas surcharger le CPU

    print("Fin du programme.")

if __name__ == "__main__":
    asyncio.run(main())