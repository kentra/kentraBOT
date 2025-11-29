import asyncio
from bleak import BleakClient, BleakScanner

# --- CONFIGURATION ---
# PASTE YOUR MAC-SPECIFIC UUID HERE (e.g. "CC:76:83:...")

DEVICE_UUID = "F8A4D5AA-09DD-9B95-A689-6AAB6042EDAF"
WRITE_CHAR_UUID = "0000ae3b-0000-1000-8000-00805f9b34fb"


async def main():
    print(f"Searching for {DEVICE_UUID}...")
    # Force disconnection from any previous lingering sessions
    device = await BleakScanner.find_device_by_address(DEVICE_UUID, timeout=10.0)

    if not device:
        print("❌ Device not found.")
        print("1. Unplug the battery box and plug it back in (Reset).")
        print("2. Turn OFF Bluetooth on your iPhone.")
        return

    print("Connecting...")
    async with BleakClient(device) as client:
        print("✅ Connected!")
        print("I will now try 4 different protocols. Watch the motor!")
        print("-" * 40)

        # --- PROTOCOL 1: MOULD KING / QY (Standard) ---
        # Format: [0xAD, MotA, MotB, MotC, MotD, Checksum]
        # 0x80 = Stop, 0xFF = Fwd, 0x00 = Rev
        print("▶️ TRYING PROTOCOL 1 (Mould King Standard)...")
        # Calc: AD + FF + 80 + 80 + 80 = 24C -> Checksum 4C
        payload_1 = bytes([0xAD, 0xFF, 0x80, 0x80, 0x80, 0x4C])
        await client.write_gatt_char(WRITE_CHAR_UUID, payload_1)
        await asyncio.sleep(1.5)

        # Stop 1
        await client.write_gatt_char(
            WRITE_CHAR_UUID, bytes([0xAD, 0x80, 0x80, 0x80, 0x80, 0xCB])
        )
        print("   (Stopped Protocol 1)")
        await asyncio.sleep(1)

        # --- PROTOCOL 2: OLD QY (Simple) ---
        # Format: [0xA1, Port, Speed, Checksum]
        print("▶️ TRYING PROTOCOL 2 (Old QY)...")
        # Calc: A1 + 01 + 64 = 106 -> Checksum 06
        payload_2 = bytes([0xA1, 0x01, 0x64, 0x06])
        await client.write_gatt_char(WRITE_CHAR_UUID, payload_2)
        await asyncio.sleep(1.5)

        # Stop 2
        await client.write_gatt_char(WRITE_CHAR_UUID, bytes([0xA1, 0x01, 0x00, 0xA2]))
        print("   (Stopped Protocol 2)")
        await asyncio.sleep(1)

        # --- PROTOCOL 3: DUAL-BYTE (Alternative) ---
        # Format: [0xFF, Port, Speed] (No checksum)
        print("▶️ TRYING PROTOCOL 3 (Simple Hex)...")
        payload_3 = bytes([0xFF, 0x01, 0xFF])
        await client.write_gatt_char(WRITE_CHAR_UUID, payload_3)
        await asyncio.sleep(1.5)

        # Stop 3
        await client.write_gatt_char(WRITE_CHAR_UUID, bytes([0xFF, 0x01, 0x00]))
        print("   (Stopped Protocol 3)")
        await asyncio.sleep(1)

        # --- PROTOCOL 4: CaDA (Complex) ---
        # Format: [0x75, 0xA5, MotA, MotB, MotC, MotD, Check]
        print("▶️ TRYING PROTOCOL 4 (CaDA)...")
        payload_4 = bytes([0x75, 0xA5, 0x80, 0x00, 0x00, 0x00, 0x00])  # 0x80 = Speed
        await client.write_gatt_char(WRITE_CHAR_UUID, payload_4)
        await asyncio.sleep(1.5)

        print("-" * 40)
        print("Test Complete. Which one moved the motor?")


asyncio.run(main())
