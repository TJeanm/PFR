import asyncio
from bleak import BleakClient

class BluetoothCommunication:
    def __init__(self, mac_address, uuid, end_marker="\n"):
        self.mac_address = mac_address
        self.uuid = uuid
        self.client = None
        self.connected = False
        self.chunk_size = 32  # Limite classique BLE
        self.received_messages = []  # Liste des messages reçus
        self.message_received_event = asyncio.Event()  # Événement pour signaler un message complet
        self.current_message = ""  # Buffer pour stocker le message en cours
        self.end_marker = end_marker  # Caractère indiquant la fin du message

    async def init_connexion(self):
        """ Initialise la connexion Bluetooth """
        self.client = BleakClient(self.mac_address)
        await self.client.connect()
        self.connected = self.client.is_connected

        if self.connected:
            print(f"✅ Connecté à {self.mac_address}")
            await self.client.start_notify(self.uuid, self.notification_handler)
        else:
            print("❌ Échec de la connexion")

    async def send_message(self, message):
        """ Envoie un message en trames de 32 octets """
        if not self.connected:
            print("⚠️ Impossible d'envoyer, non connecté.")
            return
        
        for i in range(0, len(message), self.chunk_size):
            chunk = message[i:i+self.chunk_size]
            try:
                await self.client.write_gatt_char(self.uuid, chunk.encode(), response=True)
            except Exception as e:
                print(f"⚠️ Erreur d'envoi : {e}")
                break

    def notification_handler(self, sender, data):
        """ Gère la réception des messages fragmentés et les reconstruit """
        try:
            fragment = data.decode(errors="ignore")  # Décode le fragment reçu
            self.current_message += fragment  # Ajoute le fragment au buffer

            if self.end_marker in self.current_message:  # Vérifie si le message est complet
                full_message, self.current_message = self.current_message.split(self.end_marker, 1)
                self.received_messages.append(full_message.strip())  # Stocke le message complet
                self.message_received_event.set()  # Déclenche l'événement
        except Exception as e:
            print(f"⚠️ Erreur de décodage : {e}")

    async def wait_for_message(self, timeout=10):
        """ Attend qu'un message complet soit reçu ou que le timeout expire """
        try:
            await asyncio.wait_for(self.message_received_event.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            print("⏳ Timeout : aucun message reçu.")
        finally:
            self.message_received_event.clear()  # Réinitialiser l'événement

    async def close_connexion(self):
        """ Ferme la connexion proprement """
        if self.connected:
            await self.client.stop_notify(self.uuid)
            await self.client.disconnect()
            self.connected = False
            print("🔌 Déconnexion réussie.")

    def get_received_messages(self):
        """ Retourne la liste des messages reçus """
        temp = self.received_messages
        self.received_messages = []
        return temp

# --- Exemple d'utilisation ---
async def main():
    bt = BluetoothCommunication("D8:A9:8B:C4:08:F2", "0000ffe1-0000-1000-8000-00805f9b34fb")
    await bt.init_connexion()

    await bt.send_message("Coucou ma couille\n")
    print("⏳ En attente du message complet...")
    await bt.wait_for_message(timeout=10)  # Attend qu'un message complet soit reçu

    messages = bt.get_received_messages()
    print("📥 Messages reçus :", messages)

    await bt.close_connexion()

asyncio.run(main())
