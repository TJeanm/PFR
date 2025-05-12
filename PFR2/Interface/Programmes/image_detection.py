import subprocess
import time
import keyboard
import asyncio
from communication_HM10 import communication

CHEMIN_POSITION = "Casse_Noisette/position_balle.txt"
POS_MIN = 0
POS_MAX = 100

def lire_position():
    try:
        with open(CHEMIN_POSITION, "r") as f:
            ligne = f.readline().strip()
            x_str, y_str = ligne.split()
            x, y = int(x_str), int(y_str)
            return x, y
    except Exception:
        return 0, 0  # Valeurs par défaut en cas d'erreur

def reaction_robot(x,y):
    envoie = "m"
    if (x == 0 and y == 0) or (x == POS_MAX and y == POS_MAX):
        envoie = "d"
    elif(x <= POS_MAX/3):
        envoie = "d"
    elif(x >= POS_MAX*2/3):
        envoie = "g"
    else :
        envoie = "z"
    return envoie
    

async def main():
    print("Appuyez sur 'l' pour arrêter...")

    com = communication()
    await com.init_HM10()
    ancien_temp = 0
    while True:
        if keyboard.is_pressed('l'):
            await com.envoie_bluetooth("m")
            break

        new_temp = time.time()
        if new_temp - ancien_temp >= 0.5:
            x, y = lire_position()
            print(f"x = {x} et y = {y}")
            envoie = reaction_robot(x,y)
            await com.envoie_bluetooth(envoie)

            ancien_temp = new_temp

        time.sleep(0.02)  #  Pour ne pas surcharger le CPU

    print("Fin du programme.")

if __name__ == "__main__":
    asyncio.run(main())
