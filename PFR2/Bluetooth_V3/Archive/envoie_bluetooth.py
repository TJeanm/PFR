import asyncio
from bleak import BleakClient

# Remplace par l'adresse MAC (ou l'adresse BLE) de ton HM-10
HM10_ADDRESS = "D8:A9:8B:C4:08:F2"

# UUID de la caractéristique UART (souvent "0000ffe1-0000-1000-8000-00805f9b34fb")
UART_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

async def send_command(command: str):
    async with BleakClient(HM10_ADDRESS) as client:
        if client.is_connected:
            print(f"Connecté à {HM10_ADDRESS}")
            # On ajoute un saut de ligne à la commande pour que l'Arduino puisse la lire jusqu'au "\n"
            data = (command + "\n").encode("utf-8")
            await client.write_gatt_char(UART_CHAR_UUID, data)
            print(f"Commande envoyée : {command}")
            # Petite pause pour la transmission
            await asyncio.sleep(1)
        else:
            print("Erreur de connexion au module.")

def lecture_manette():
    lecture = ""
    with open("Com_to_Manette.txt", "r", encoding="utf-8") as fichier:
        commande = fichier.readlines()
        commande.pop()
        for valeur in commande :
            lecture = lecture + valeur.strip() + ","
        lecture = lecture  + "\n"
    return lecture

async def main():
    commande = lecture_manette()
    print(commande)
    await send_command(commande)

if __name__ == "__main__":
    asyncio.run(main())