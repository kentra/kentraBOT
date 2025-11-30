from app.models.config import AppConfig
from app.tools.hub_control import HubControl
import asyncio
from app.models.hub_models import MotorSpeed
import asyncio

cfg = AppConfig()
ctrl = HubControl(cfg)
asyncio.run(ctrl.connect())


asyncio.run(
    ctrl.run(MotorSpeed(speed_a=40, speed_b=0, speed_c=0, speed_d=40), duration=5.0)
)


# await ctrl.locate_device()

# await ctrl.run_smooth(MotorSpeed(speed_a=40, speed_b=0, speed_c=0, speed_d=0))

# ble_device: BLEDevice | None = await BleakScanner.find_device_by_address(
#             device_identifier=cfg.DEVICE_UUID, timeout=10.0
#         )
