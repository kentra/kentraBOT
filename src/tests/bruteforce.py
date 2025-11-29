import asyncio
from bleak import BleakClient, BleakScanner

# PASTE YOUR UUID HERE (From your screenshot)
# DEVICE_UUID = "D0E8CA5B-15D7-D4CB-1FD5-C2BFB001345B"
# DEVICE_UUID = "d0e8ca5b-15d7-d4cb-1fd5-c2bfb001345b"
DEVICE_UUID = "F8A4D5AA-09DD-9B95-A689-6AAB6042EDAF"
WRITE_CHAR_UUID = "0000ae3a-0000-1000-8000-00805f9b34fb"


async def main():
    print(f"Searching for device {DEVICE_UUID}...")
    device = await BleakScanner.find_device_by_address(DEVICE_UUID, timeout=10.0)

    if not device:
        print("Device not found! Make sure it is ON and not connected to your phone.")
        return

    print("Connecting...")
    async with BleakClient(device) as client:
        print(f"Connected: {client.is_connected}")

        # We will try 3 different packet structures.
        # Listen carefully to see if your motor spins!

        # TEST 1: The "Mould King / QY" Standard (Most Likely)
        # Structure: [Header, Port, Speed, Checksum]
        print("Test 1: Sending Mould King style packet (A1)...")
        payload = bytes([0xA1, 0x01, 0x64, 0x00])
        await client.write_gatt_char(WRITE_CHAR_UUID, payload)
        await asyncio.sleep(2)

        # TEST 2: The "Simple Hex" Standard
        # Structure: [Header, Port, Speed]
        print("Test 2: Sending Simple Hex packet (FF)...")
        payload = bytes([0xFF, 0x01, 0xFF])
        await client.write_gatt_char(WRITE_CHAR_UUID, payload)
        await asyncio.sleep(2)

        # TEST 3: The "CaDA" Standard
        # Structure: [Header, M1, M2, M3, M4, Check]
        print("Test 3: Sending CaDA style packet (75)...")
        payload = bytes(
            [0x75, 0xA5, 0x80, 0x80, 0x80, 0x80, 0x00]
        )  # 0x80 usually means 'Forward'
        await client.write_gatt_char(WRITE_CHAR_UUID, payload)
        await asyncio.sleep(2)

        # STOP COMMAND
        print("Stopping motors...")
        stop_payload = bytes([0xA1, 0x01, 0x00, 0x00])
        await client.write_gatt_char(WRITE_CHAR_UUID, stop_payload)


asyncio.run(main())
