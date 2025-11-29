import asyncio
from bleak import BleakClient, BleakScanner

# --- CONFIGURATION ---
# PASTE YOUR MAC-SPECIFIC UUID HERE
DEVICE_UUID = "F8A4D5AA-09DD-9B95-A689-6AAB6042EDAF"
WRITE_CHAR_UUID = "0000ae3b-0000-1000-8000-00805f9b34fb"

# --- CONSTANTS ---
DEADZONE = 25  # The motor needs at least ~25 power to start moving


def build_packet(speed_a, speed_b, speed_c, speed_d):
    """
    Converts percentage (-100 to 100) into Signed 8-bit Integers.
    """

    def map_signed(percent):
        # 1. Handle STOP
        if percent == 0:
            return 0

        # 2. Clamp Input
        percent = max(-100, min(100, percent))

        # 3. Scale with Deadzone
        # We need to map 1..100% to 25..127 (approx)
        usable_range = 127 - DEADZONE

        if percent > 0:
            # Positive (Forward)
            val = DEADZONE + (percent / 100.0 * usable_range)
            return int(val)
        else:
            # Negative (Backward)
            # We calculate positive magnitude first, then flip to negative
            mag = DEADZONE + (abs(percent) / 100.0 * usable_range)
            val = -int(mag)

            # Convert negative number to unsigned byte (Two's Complement)
            # e.g. -100 becomes 156 (0x9C)
            return val & 0xFF

    # Map the speeds
    byte_a = map_signed(speed_a)
    byte_b = map_signed(speed_b)  # Port C?
    byte_c = map_signed(speed_c)  # Port B?
    byte_d = map_signed(speed_d)

    # Calculate Checksum
    # Simple sum of the 4 motor bytes
    checksum = (byte_a + byte_b + byte_c + byte_d) & 0xFF

    # Header AB CD 01 ...
    return bytes([0xAB, 0xCD, 0x01, byte_a, byte_b, byte_c, byte_d, checksum])


async def main():
    print(f"Connecting to {DEVICE_UUID}...")
    device = await BleakScanner.find_device_by_address(DEVICE_UUID, timeout=10.0)

    if not device:
        print("❌ Device not found.")
        return

    async with BleakClient(device) as client:
        print("✅ Connected!")
        print("Stopping first (sending 0x00)...")
        await client.write_gatt_char(WRITE_CHAR_UUID, build_packet(0, 0, 0, 0))
        await asyncio.sleep(1)

        print("🚀 Ramping UP Forward (0 -> 100%)...")
        for s in range(0, 101, 5):
            print(f"   Speed: {s}%")
            await client.write_gatt_char(WRITE_CHAR_UUID, build_packet(s, 0, 0, 0))
            await asyncio.sleep(0.1)

        print("🛑 STOP (2 sec)...")
        await client.write_gatt_char(WRITE_CHAR_UUID, build_packet(0, 0, 0, 0))
        await asyncio.sleep(2)

        print("🔙 Ramping UP Reverse (0 -> -100%)...")
        for s in range(0, 101, 5):
            print(f"   Speed: -{s}%")
            await client.write_gatt_char(WRITE_CHAR_UUID, build_packet(-s, 0, 0, 0))
            await asyncio.sleep(0.1)

        print("🛑 Final STOP.")
        await client.write_gatt_char(WRITE_CHAR_UUID, build_packet(0, 0, 0, 0))


asyncio.run(main())
