import keyboard

def main():
    import keyboard
import asyncio
from bleak import BleakClient, BleakScanner

UART_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
TARGET_NAME    = "robot2"
SCAN_TIMEOUT   = 5.0    # secondes

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

    # 3) Envoie de la donnée
    data = f"p\n".encode()
    # response=False pour ne pas attendre l'ACK
    await client.write_gatt_char(
        UART_CHAR_UUID, data, response=False
    )
    print(f"📤 Envoyé : p")
    await asyncio.sleep(0.1)

    # subprocess.run(["python", os.getcwd()+ "\\Programmes\\test_pilotage.py"]) 
    while True:
        if keyboard.is_pressed('l'):
            data = f"l\n".encode()
            # response=False pour ne pas attendre l'ACK
            await client.write_gatt_char(
                UART_CHAR_UUID, data, response=False
            )
            print(f"📤 Envoyé : l")
            await asyncio.sleep(0.1)
            print("Test fini")
            break

if __name__ == "__main__":
    asyncio.run(main())