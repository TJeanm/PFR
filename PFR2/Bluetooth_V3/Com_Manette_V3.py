import asyncio
import sys
import pygame
from bleak import BleakClient, BleakScanner

UART_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
TARGET_NAME = "robot2"
SCAN_TIMEOUT = 5.0  # secondes

# Vos commandes
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

# seuil de deadzone : tout |axe| < 0.2 est considéré 0
DEADZONE = 0.2
# délai de boucle ramené à 20 ms
LOOP_DELAY = 0.02


async def main():
    # 1) scan 5 s
    print(f"🔍 Recherche de « {TARGET_NAME} » ({SCAN_TIMEOUT}s)...")
    devices = await BleakScanner.discover(timeout=SCAN_TIMEOUT)
    target = next((d for d in devices
                   if d.name and d.name.lower() == TARGET_NAME.lower()), None)
    if not target:
        print(f"❌ Aucun périphérique nommé {TARGET_NAME}.")
        return

    # 2) Connexion BLE
    print(f"🔗 Connexion à {target.name} [{target.address}]…")
    async with BleakClient(target.address) as client:
        if not client.is_connected:
            print("❌ Échec de connexion.")
            return
        print("✅ Connecté.")

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

                # logique de choix de cmd (idem votre code)
                if btn[2] == 1:
                    cmd = MODE_AUTO
                elif btn[1] == 1:
                    cmd = MODE_MANUEL
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
                    data = f"{cmd}\n".encode()
                    # response=False pour ne pas attendre l'ACK
                    await client.write_gatt_char(
                        UART_CHAR_UUID, data, response=False
                    )
                    print(f"📤 Envoyé : {cmd}")
                    last_cmd = cmd

                await asyncio.sleep(LOOP_DELAY)

        except (btn[2] == 1):
            print("\n🛑 Arrêt demandé par l'utilisateur.")
        finally:
            pygame.quit()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
