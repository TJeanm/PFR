import keyboard
import asyncio
from communication_HM10 import communication

async def main():
    com = communication()
    await com.init_HM10()
    await com.envoie_bluetooth("o")
    while True:
        if keyboard.is_pressed('l'):
            await com.envoie_bluetooth("l")
            print("Test fini")
            break

if __name__ == "__main__":
    asyncio.run(main())