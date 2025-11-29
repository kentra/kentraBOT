import asyncio
from bleak import BleakClient, BleakScanner

# --- CONFIGURATION ---
# 1. If on Mac, paste the UUID from your screenshot below.
# 2. If on Windows, run a scan first to get the MAC address (e.g., "A1:B2:C3:D4:E5:F6")
# DEVICE_ID = "D0E8CA5B-15D7-D4CB-1FD5-C2BFB001345B"

# The IDs found in your screenshot (standard base UUID + short ID)
# WRITE_CHAR_UUID = "0000ae3b-0000-1000-8000-00805f9b34fb"
DEVICE_ID = "F8A4D5AA-09DD-9B95-A689-6AAB6042EDAF"
WRITE_CHAR_UUID = "0000ae3b-0000-1000-8000-00805f9b34fb"


async def main():
    print(f"Searching for {DEVICE_ID}...")
    device = await BleakScanner.find_device_by_address(DEVICE_ID, timeout=10.0)

    if not device:
        print(f"Could not find device with ID: {DEVICE_ID}")
        print(
            "If you are on Windows/Linux, you cannot use the iOS UUID. You must scan for the MAC address."
        )
        return

    print("Connecting...")
    async with BleakClient(device) as client:
        print(f"Connected: {client.is_connected}")

        # --- PROTOCOL TEST AREA ---
        # These boards usually use one of these two command formats.
        # Try uncommenting one, running it, and seeing if a motor moves.

        # OPTION A: Common 'Mould King' / Generic Protocol
        # Format: [Header, Port, Speed, Checksum/Padding]
        # 0xA1 = Header, 0x01 = Port A, 0x64 = Speed 100 (Forward), 0x00 = Padding
        payload_A = bytes([0xA1, 0x01, 0x64, 0x00])

        # OPTION B: Simple Hex Protocol
        # Format: [Header, Command, Speed]
        # 0xFF = Header, 0x01 = Port 1, 0xFF = Max Speed
        payload_B = bytes([0xFF, 0x01, 0xFF])

        # OPTION C: The "CaDA" Protocol
        # Format: [Header, A_Speed, B_Speed, C_Speed, D_Speed, Checksum]
        # 0x00 = Stop, 0x80 = Forward Max, 0x7F = Backward Max
        payload_C = bytes([0x75, 0xA5, 0x00, 0x80, 0x00, 0x00, 0x00])  # 0x80 is speed

        print("Sending Test Command (Option A)...")
        await client.write_gatt_char(WRITE_CHAR_UUID, payload_A)

        await asyncio.sleep(2)  # Run for 2 seconds

        print("Stopping...")
        # Send stop command (usually speed 0)
        stop_payload = bytes([0xA1, 0x01, 0x00, 0x00])
        await client.write_gatt_char(WRITE_CHAR_UUID, stop_payload)


asyncio.run(main())
