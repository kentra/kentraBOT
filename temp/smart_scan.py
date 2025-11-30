import asyncio
from bleak import BleakClient, BleakScanner

# --- CONFIGURATION ---
DEVICE_UUID = "F8A4D5AA-09DD-9B95-A689-6AAB6042EDAF"
WRITE_CHAR_UUID = "0000ae3b-0000-1000-8000-00805f9b34fb"


async def main():
    print(f"Connecting to {DEVICE_UUID}...")
    async with BleakClient(DEVICE_UUID) as client:
        print("Connected! Starting Header Scan...")
        print("WATCH YOUR MOTOR. If it spins, press Ctrl+C immediately!")

        # We will scan all 256 possible headers
        for header in range(0, 256):
            # ATTEMPT 1: The "Simple" Structure (Used by 70% of clones)
            # Format: [Header, Port(1), Speed(100), Checksum]
            # Checksum usually = Sum of bytes % 255
            checksum = (header + 0x01 + 0x64) & 0xFF
            payload = bytes([header, 0x01, 0x64, checksum])

            # ATTEMPT 2: The "Mould King" Structure (If Attempt 1 is quiet)
            # Format: [Header, SpeedA, SpeedB, SpeedC, SpeedD, Checksum]
            # mk_checksum = (header + FF + 80 + 80 + 80) & 0xFF
            # mk_payload = bytes([header, 0xFF, 0x80, 0x80, 0x80, mk_checksum])

            # We send Attempt 1 first (It's most common for this board layout)
            try:
                await client.write_gatt_char(WRITE_CHAR_UUID, payload, response=False)
                # If you want to try Attempt 2 simultaneously, uncomment the next line:
                # await client.write_gatt_char(WRITE_CHAR_UUID, mk_payload, response=False)
            except Exception as e:
                print(f"Error on header {hex(header)}: {e}")

            # Print status every 10 headers so you know where we are
            if header % 10 == 0:
                print(f"Scanning Header: {hex(header)}...")

            # Go fast! 0.05s per try
            await asyncio.sleep(0.05)

        print("Scan complete. Did it move?")


asyncio.run(main())
