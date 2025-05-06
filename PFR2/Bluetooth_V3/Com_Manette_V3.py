import asyncio
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from bleak import BleakClient
import pygame

# Adresse MAC du HM-10
HM10_ADDRESS = "D8:A9:8B:C4:08:F2"

# UUID de la caractéristique UART
UART_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

# Définition des commandes
ARRET = "m"
AVANCE = "z"
RECULE = "s"
DROITE = "d"
GAUCHE = "q"
AVANCE_GAUCHE = "a"
AVANCE_DROITE = "e"
RECULE_GAUCHE = "w"
RECULE_DROITE = "x"

AVANCE_RAPIDE = "t"
RECULE_RAPIDE = "g"
GAUCHE_RAPIDE = "f"
DROITE_RAPIDE = "h"
AVANCE_GAUCHE_RAPIDE = "r"
AVANCE_DROITE_RAPIDE = "y"
RECULE_GAUCHE_RAPIDE = "v"
RECULE_DROITE_RAPIDE = "b"


class BluetoothCommunication:
    def __init__(self, adresse_mac, uuid):
        print("Test init start")
        self.adresse_mac = adresse_mac
        self.uuid = uuid
        self.client = None
        self.transmission = ""
        self.last_transmission = None
        self.joystick = None

    async def init_HM10(self):
        print("Test init HM10")
        self.client = BleakClient(self.adresse_mac)
        try:
            await self.client.connect()
            #await self.client.get_services()
            if self.client.is_connected:
                print(f"✅ Connecté à {self.adresse_mac}")
                data = (self.transmission + "\n").encode("utf-8")
                await self.client.write_gatt_char(UART_CHAR_UUID, data)
            else:
                print("❌ Échec de connexion au module Bluetooth.")
        except Exception as e:
            print(f"Erreur de connexion Bluetooth : {e}")

    def init_Manette(self):
        print("Test init Manette")
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Manette détectée : {self.joystick.get_name()}")
        else:
            print("Aucune manette détectée")
            exit()

    def lecture_manette(self):
        pygame.event.pump()
        transmissionValue = ""
        value_btn = [0] * self.joystick.get_numbuttons()
        value_joy = [0] * self.joystick.get_numaxes()

        for i in range(self.joystick.get_numbuttons()):
            value_btn[i] = self.joystick.get_button(i)

        for i in range(self.joystick.get_numaxes()):
            value = self.joystick.get_axis(i)
            if value > 0.8:
                value = 1
            elif value < -0.8:
                value = -1
            else:
                value = 0
            value_joy[i] = value

        # 🔴 Arrêt immédiat si bouton [2] est pressé
        if value_btn[2] == 1:
            print("🛑 Bouton [2] pressé : arrêt du programme.")
            raise KeyboardInterrupt

        # Choix de la commande
        if value_btn[10] == 0:
            if value_joy[1] == -1:
                if value_joy[2] == 1:
                    transmissionValue = AVANCE_DROITE
                elif value_joy[2] == -1:
                    transmissionValue = AVANCE_GAUCHE
                else:
                    transmissionValue = AVANCE
            elif value_joy[1] == 1:
                if value_joy[2] == 1:
                    transmissionValue = RECULE_DROITE
                elif value_joy[2] == -1:
                    transmissionValue = RECULE_GAUCHE
                else:
                    transmissionValue = RECULE
            elif value_joy[2] == 1:
                transmissionValue = DROITE
            elif value_joy[2] == -1:
                transmissionValue = GAUCHE
            else:
                transmissionValue = ARRET
        else:
            if value_joy[1] == -1:
                if value_joy[2] == 1:
                    transmissionValue = AVANCE_DROITE_RAPIDE
                elif value_joy[2] == -1:
                    transmissionValue = AVANCE_GAUCHE_RAPIDE
                else:
                    transmissionValue = AVANCE_RAPIDE
            elif value_joy[1] == 1:
                if value_joy[2] == 1:
                    transmissionValue = RECULE_DROITE_RAPIDE
                elif value_joy[2] == -1:
                    transmissionValue = RECULE_GAUCHE_RAPIDE
                else:
                    transmissionValue = RECULE_RAPIDE
            elif value_joy[2] == 1:
                transmissionValue = DROITE_RAPIDE
            elif value_joy[2] == -1:
                transmissionValue = GAUCHE_RAPIDE
            else:
                transmissionValue = ARRET

        self.transmission = transmissionValue

    async def loop(self):
        try:
            while True:
                self.lecture_manette()
                if self.transmission != self.last_transmission:
                    await self.init_HM10()
                    #data = (self.transmission + "\n").encode("utf-8")
                    #await self.client.write_gatt_char(UART_CHAR_UUID, data)
                    print(f"Commande envoyée : {self.transmission}")
                    self.last_transmission = self.transmission  
                await asyncio.sleep(0.1)
        except KeyboardInterrupt:
            print("🛑 Arrêt du programme par l'utilisateur")
        finally:
            pygame.quit()


async def main():
    BC = BluetoothCommunication(HM10_ADDRESS, UART_CHAR_UUID)
    #await BC.init_HM10()
    BC.init_Manette()
    await BC.loop()

asyncio.run(main())
