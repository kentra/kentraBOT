import asyncio
from bleak import BleakScanner


async def scan():
    print("Scanning... (Ensure iPhone Bluetooth is OFF)")
    devices = await BleakScanner.discover()

    found = False
    for d in devices:
        # We filter for devices that have a name, as these boards usually broadcast one
        if d.name and d.name != "Unknown":
            print(f"FOUND: {d.name}")
            print(f"  UUID: {d.address}")  # On Mac, this is the UUID you need
            print("-" * 20)
            found = True

    if not found:
        print("No named devices found. Try moving the controller closer.")


if __name__ == "__main__":
    asyncio.run(scan())
