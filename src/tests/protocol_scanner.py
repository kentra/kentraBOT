import asyncio
from bleak import BleakClient, BleakScanner

# --- CONFIGURATION ---
# PASTE YOUR MAC-SPECIFIC UUID HERE
# (Run a scan if you don't have it, e.g., "A1:B2:C3:...")
DEVICE_UUID = "F8A4D5AA-09DD-9B95-A689-6AAB6042EDAF"

WRITE_CHAR_UUID = "0000ae3b-0000-1000-8000-00805f9b34fb"


async def main():
    print(f"Searching for {DEVICE_UUID}...")
    device = await BleakScanner.find_device_by_address(DEVICE_UUID, timeout=10.0)

    if not device:
        print("❌ Device not found. Did you do the Hard Reset?")
        return

    async with BleakClient(device) as client:
        print("✅ Connected!")
        print("Starting 'Smart Scan' for QY-V3 Protocols...")
        print("WATCH THE MOTOR!")

        # --- ATTEMPT 1: The "Enable" Handshake (Newer V3 Boards) ---
        # Some boards ignore everything until they receive this "Hello".
        print("1. Sending Handshake/Enable command...")
        await client.write_gatt_char(WRITE_CHAR_UUID, bytes([0xFF, 0x00, 0x00, 0x00]))
        await asyncio.sleep(0.5)

        # --- ATTEMPT 2: Protocol A (Standard QY) ---
        # Header A1, Port 1, Speed 100
        print("2. Trying Protocol A (Header A1)...")
        # Checksum often: (Header + Port + Speed) AND 0xFF
        # A1 + 01 + 64 = 106 -> [A1, 01, 64, 06] (Sometimes XOR is used)
        await client.write_gatt_char(WRITE_CHAR_UUID, bytes([0xA1, 0x01, 0x64, 0x06]))
        await asyncio.sleep(1.5)

        # --- ATTEMPT 3: Protocol B (Mould King) ---
        # Header AD, FF=Fwd
        print("3. Trying Protocol B (Header AD)...")
        await client.write_gatt_char(
            WRITE_CHAR_UUID, bytes([0xAD, 0xFF, 0x80, 0x80, 0x80, 0x4C])
        )
        await asyncio.sleep(1.5)

        # --- ATTEMPT 4: Protocol C (CaDA/Double Eagle) ---
        # Header 75, A5 preamble
        print("4. Trying Protocol C (Header 75)...")
        await client.write_gatt_char(
            WRITE_CHAR_UUID, bytes([0x75, 0xA5, 0x80, 0x00, 0x00, 0x00, 0x00])
        )
        await asyncio.sleep(1.5)

        # --- ATTEMPT 5: Protocol D (The "Encryption" Hack) ---
        # Some QY V3 boards use a static XOR key.
        # This is a raw 'Forward' command recorded from a working QY-V3 unit.
        print("5. Trying Protocol D (Raw Dump)...")
        await client.write_gatt_char(WRITE_CHAR_UUID, bytes.fromhex("AA 55 01 64 00"))
        await asyncio.sleep(1.5)

        print("Scan complete. Stopping...")
        # Try to stop using the most common format
        await client.write_gatt_char(WRITE_CHAR_UUID, bytes([0xA1, 0x01, 0x00, 0xA2]))


asyncio.run(main())
