import asyncio
from bleak import BleakScanner


async def scan():
    print("Scanning for devices...")
    devices = await BleakScanner.discover()
    for d in devices:
        # Filter for likely names or just print all
        print(f"Device: {d.name}, Address: {d.address}")


asyncio.run(scan())
