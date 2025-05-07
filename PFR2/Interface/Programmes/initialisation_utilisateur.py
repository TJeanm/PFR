import asyncio
from communication_HM10 import communication

async def main():
    com = communication()
    await com.init_HM10()

if __name__ == "__main__":
    asyncio.run(main())