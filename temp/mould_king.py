import asyncio
from bleak import BleakClient, BleakScanner

# --- CONFIGURATION ---
# PASTE YOUR MAC-SPECIFIC UUID HERE
# (Run the scan script again if you lost it)


DEVICE_UUID = "F8A4D5AA-09DD-9B95-A689-6AAB6042EDAF"
WRITE_CHAR_UUID = "0000ae3b-0000-1000-8000-00805f9b34fb"


def calculate_checksum(data):
    # Mould King checksum is usually the sum of bytes (sometimes & 0xFF)
    return sum(data) & 0xFF


async def main():
    print(f"Connecting to {DEVICE_UUID}...")
    async with BleakClient(DEVICE_UUID) as client:
        print("Connected.")

        # --- THE MOULD KING / QY PROTOCOL (Hypothesis) ---
        # Structure: [Header, A, B, C, D, Checksum]
        # Header: 0xAD (Common for 4.0/6.0 modules)
        # Channels: 0x80 is STOP (128). 0xFF is MAX FWD, 0x00 is MAX REV.

        # Command: Motor A Full Speed Forward
        # [0xAD, SpeedA, SpeedB, SpeedC, SpeedD, Checksum]
        # Some versions need extra padding bytes. We will try the standard 6-byte first.

        header = 0xAD
        speed_A = 0xFF  # Full Forward
        speed_B = 0x80  # Stop
        speed_C = 0x80  # Stop
        speed_D = 0x80  # Stop

        payload = [header, speed_A, speed_B, speed_C, speed_D]
        checksum = calculate_checksum(payload)
        payload.append(checksum)

        data = bytes(payload)

        print(f"Sending: {data.hex()}")
        await client.write_gatt_char(WRITE_CHAR_UUID, data)

        await asyncio.sleep(2)

        # STOP
        print("Stopping...")
        stop_payload = [0xAD, 0x80, 0x80, 0x80, 0x80]
        stop_check = calculate_checksum(stop_payload)
        stop_payload.append(stop_check)

        await client.write_gatt_char(WRITE_CHAR_UUID, bytes(stop_payload))


asyncio.run(main())
