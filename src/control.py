import asyncio
from bleak import BleakClient

# REPLACE THESE WITH YOUR VALUES
DEVICE_ADDRESS = "AA:BB:CC:DD:EE:FF"  # Or UUID on Mac
# The UUID usually looks like "0000xxxx-0000-1000-8000-00805f9b34fb"
# You find this in the nRF Connect app under the Service.
# WRITE_CHARACTERISTIC_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
WRITE_CHARACTERISTIC_UUID = "D0E8CA5B-15D7-D4CB-1FD5-C2BFB001345B"


async def run_motor():
    async with BleakClient(DEVICE_ADDRESS) as client:
        if await client.is_connected():
            print(f"Connected to {DEVICE_ADDRESS}")

            # Example: Sending a hex payload
            # Let's say we found out 'A1 01 64' turns motor 1 on.
            # We must send it as a bytearray.
            payload = bytearray([0xA1, 0x01, 0x64])

            print(f"Sending: {payload.hex()}")

            # write_gatt_char is how we send data
            await client.write_gatt_char(WRITE_CHARACTERISTIC_UUID, payload)

            # Keep running for 2 seconds
            await asyncio.sleep(2)

            # Send Stop Command (example: speed 0)
            stop_payload = bytearray([0xA1, 0x01, 0x00])
            await client.write_gatt_char(WRITE_CHARACTERISTIC_UUID, stop_payload)
            print("Motor stopped")


asyncio.run(run_motor())
