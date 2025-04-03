import asyncio
from bleak import BleakClient
import pygame
import time
import subprocess
import os

# Adresse MAC du HM-10
HM10_ADDRESS = "D8:A9:8B:C4:08:F2"

# UUID de la caractéristique UART
UART_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

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


class BluetoothCommunication :
    def __init__(self, adresse_mac, uuid):
        print("Test init start")
        # HM10
        self.adresse_mac = adresse_mac
        self.uuid = uuid
        self.client = None
        # Manette
        self.transmission = ""
        self.joystick = None


    async def init_HM10(self):
        print("Test init HM10")
        self.client = BleakClient(self.adresse_mac)
        await self.client.connect()
        if self.client.is_connected:
            print(f"Connecté à {self.adresse_mac}")
        else:
            print("Erreur de connexion au module.")

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

    def lecture_manette(self) :
        pygame.event.pump()
        transmissionValue = ""
        value_btn = [0] * self.joystick.get_numbuttons()  # Crée une liste de la bonne taille remplie de 0
        value_joy = [0] * self.joystick.get_numaxes()  # Idem pour les joysticks
        for i in range(self.joystick.get_numbuttons()):
            value_btn[i] = self.joystick.get_button(i)
        for i in range(self.joystick.get_numaxes()):
            value = self.joystick.get_axis(i)
            if value > 0.8:
                value = 1
            elif value < -0.8:
                value = -1
            else :
                value = 0

            value_joy[i] = value

        # Choix de la commande à exécuter (value_btn[10] rend plus rapide)
        if value_btn[10] == 0 :
            if value_joy[1] == -1 :
                if value_joy[2] == 1 :
                    transmissionValue = AVANCE_DROITE
                elif value_joy[2] == -1 :
                    transmissionValue = AVANCE_GAUCHE
                else :
                    transmissionValue = AVANCE

            elif value_joy[1] == 1 :
                if value_joy[2] == 1 :
                    transmissionValue = RECULE_DROITE
                elif value_joy[2] == -1 :
                    transmissionValue = RECULE_GAUCHE
                else :
                    transmissionValue = RECULE
            elif value_joy[2] == 1 :
                transmissionValue = DROITE
            elif value_joy[2] == -1 :
                transmissionValue = GAUCHE
            else :
                transmissionValue = ARRET

        else :
            if value_joy[1] == -1 :
                if value_joy[2] == 1 :
                    transmissionValue = AVANCE_DROITE_RAPIDE
                elif value_joy[2] == -1 :
                    transmissionValue = AVANCE_GAUCHE_RAPIDE
                else :
                    transmissionValue = AVANCE_RAPIDE

            elif value_joy[1] == 1 :
                if value_joy[2] == 1 :
                    transmissionValue = RECULE_DROITE_RAPIDE
                elif value_joy[2] == -1 :
                    transmissionValue = RECULE_GAUCHE_RAPIDE
                else :
                    transmissionValue = RECULE_RAPIDE
            elif value_joy[2] == 1 :
                transmissionValue = DROITE_RAPIDE
            elif value_joy[2] == -1 :
                newVtransmissionValuealue = GAUCHE_RAPIDE
            else :
                transmissionValue = ARRET
        self.transmission = transmissionValue

    async def loop(self):
        try:
            while True:
                self.lecture_manette(self)
                data = (self.transmission + "\n").encode("utf-8")
                await self.client.write_gatt_char(UART_CHAR_UUID, data)
                print(f"Commande envoyée : {self.transmission}")
                # Petite pause pour la transmission
                await asyncio.sleep(1)
        except KeyboardInterrupt :
            print("🛑 Arrêt du programme")
        finally:
            pygame.quit()

async def main():
    BC = BluetoothCommunication(HM10_ADDRESS, UART_CHAR_UUID)
    await BC.init_HM10()
    BC.init_Manette()
    await BC.loop()

asyncio.run(main())