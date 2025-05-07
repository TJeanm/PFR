import asyncio
import sys
from bleak import BleakClient, BleakScanner


UART_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
TARGET_NAME    = "robot2"
SCAN_TIMEOUT   = 5.0
LOOP_DELAY = 0.1 

class communication :
    def __init__(self):
        self.client  = None
        self.transmiton = ""
        

    async def init_HM10(self):
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        print(f"🔍 Recherche de « {TARGET_NAME} » ({SCAN_TIMEOUT}s)...")
        devices = await BleakScanner.discover(timeout=SCAN_TIMEOUT)
        target = next((d for d in devices if d.name and d.name.lower() == TARGET_NAME.lower()), None)
        if not target:
            print(f"❌ Aucun périphérique nommé {TARGET_NAME}.")
            return

        print(f"🔗 Connexion à {target.name} [{target.address}]…")
        self.client = BleakClient(target.address)
        await self.client.connect()

        if not self.client.is_connected:
            print("❌ Échec de connexion.")
            return
        print("✅ Connecté.")

        await self.envoie_bluetooth("l")


    async def envoie_bluetooth(self, lettre) :
        data = f"{lettre}\n".encode()
        # response=False pour ne pas attendre l'ACK
        await self.client.write_gatt_char(UART_CHAR_UUID, data, response=False)
        print(f"📤 Envoyé : {lettre}")
        await asyncio.sleep(LOOP_DELAY)
    
    async def close(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            print("🔌 Déconnecté.")
