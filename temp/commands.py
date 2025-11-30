import asyncio
from bleak import BleakClient, BleakScanner

# --- CONFIGURATION ---
# PASTE YOUR MAC-SPECIFIC UUID HERE
DEVICE_UUID = "F8A4D5AA-09DD-9B95-A689-6AAB6042EDAF"

# The Characteristic you found
WRITE_CHAR_UUID = "0000ae3b-0000-1000-8000-00805f9b34fb"


def build_packet(
    speed_a: int = 0, speed_b: int = 0, speed_c: int = 0, speed_d: int = 0
):
    """
    Converts speeds (-100 to 100) into the AB CD 01 protocol.
    """

    # 1. Helper to map -100/100 to 0-255 (where 128 is 0)
    def map_speed(val):
        # Clamp value between -100 and 100
        val = max(-100, min(100, val))
        # Map: -100 -> 0, 0 -> 128, 100 -> 255
        # The math: 128 + (val * 1.27)
        return int(128 + (val * 1.27))

    hex_a = map_speed(val=speed_a)
    hex_b = map_speed(val=speed_b)
    hex_c = map_speed(val=speed_c)
    hex_d = map_speed(val=speed_d)

    # 2. Calculate Checksum
    # Based on your logs, Checksum = Sum of the 4 motor bytes only
    checksum = (hex_a + hex_b + hex_c + hex_d) & 0xFF

    # 3. Build the Byte Array
    # Structure: AB CD 01 [A] [B] [C] [D] [Checksum]
    packet = bytes([0xAB, 0xCD, 0x01, hex_a, hex_b, hex_c, hex_d, checksum])

    return packet


async def main():
    print(f"Searching for {DEVICE_UUID}...")
    device = await BleakScanner.find_device_by_address(DEVICE_UUID, timeout=10.0)

    if not device:
        print("❌ Device not found. Check Bluetooth settings.")
        return

    async with BleakClient(device) as client:
        print("✅ Connected!")

        # --- COMMANDS ---

        print("🚀 Motor A: Forward 50%...")
        # Note: Your logs showed 'C' was the 2nd byte, so we map: A, C, B, D
        # Packet format: A, C, B, D
        cmd = build_packet(speed_a=10)
        print(f"Sending: {cmd.hex()}")
        await client.write_gatt_char(WRITE_CHAR_UUID, cmd)
        await asyncio.sleep(2)

        # print("🔙 Motor A: Backward 50%...")
        # cmd = build_packet(speed_a=-50, speed_b=0, speed_c=0, speed_d=0)
        # await client.write_gatt_char(WRITE_CHAR_UUID, cmd)
        # await asyncio.sleep(2)

        # print("🚀 Motor C: Forward 100% (Turbo)...")
        # # Controlling the 2nd byte (which acts as C on your board)
        # cmd = build_packet(speed_a=0, speed_b=100, speed_c=0, speed_d=0)
        # await client.write_gatt_char(WRITE_CHAR_UUID, cmd)
        # await asyncio.sleep(2)

        print("🛑 STOP...")
        stop_cmd = build_packet(0, 0, 0, 0)
        await client.write_gatt_char(WRITE_CHAR_UUID, stop_cmd)


asyncio.run(main())
