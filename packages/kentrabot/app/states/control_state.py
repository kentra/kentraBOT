import reflex as rx
from app.states.config_state import ConfigState
from app.states.log_state import LogState


class ControlState(rx.State):
    target_speed: int = 0
    directional_bias: int = 0
    is_motor_running: bool = False
    emergency_stop_active: bool = False
    show_estop_confirm: bool = False
    camera_connected: bool = False
    drone_altitude: float = 0.0
    drone_heading: int = 0
    active_keys: dict[str, bool] = {}

    @rx.var
    def connection_status_text(self) -> str:
        return "Connected" if self.camera_connected else "Disconnected"

    @rx.var
    def connection_status_color(self) -> str:
        return "text-[#08C6AB]" if self.camera_connected else "text-red-500"

    @rx.event
    async def toggle_camera(self):
        self.camera_connected = not self.camera_connected
        logs = await self.get_state(LogState)
        if self.camera_connected:
            logs.add_log("info", "Camera", "Camera stream connected.")
            yield rx.toast("Camera stream established.", duration=2000)
        else:
            logs.add_log("warning", "Camera", "Camera stream disconnected by user.")
            yield rx.toast("Camera disconnected.", duration=2000)

    @rx.event
    def handle_key_down(self, key: str):
        """Handle key press events for drone control."""
        if self.emergency_stop_active:
            return
        key = key.lower()
        self.active_keys[key] = True
        if key == "w":
            self.drone_altitude += 0.5
        elif key == "s":
            self.drone_altitude = max(0, self.drone_altitude - 0.5)
        elif key == "arrowleft":
            self.drone_heading = (self.drone_heading - 5) % 360
        elif key == "arrowright":
            self.drone_heading = (self.drone_heading + 5) % 360
        if not self.is_motor_running and key in ["w", "s", "arrowup", "arrowdown"]:
            self.is_motor_running = True

    @rx.event
    def handle_key_up(self, key: str):
        """Handle key release events."""
        key = key.lower()
        self.active_keys[key] = False
        move_keys = ["w", "s", "arrowup", "arrowdown", "arrowleft", "arrowright"]
        if not any((self.active_keys.get(k, False) for k in move_keys)):
            self.is_motor_running = False

    @rx.event
    async def set_speed(self, value: int):
        """Set the target speed, clamped by max_speed config."""
        if self.emergency_stop_active:
            yield rx.toast("Cannot change speed: Emergency Stop Active!", duration=3000)
            return
        config_state = await self.get_state(ConfigState)
        max_limit = config_state.max_speed
        new_speed = int(value)
        if new_speed > max_limit:
            new_speed = max_limit
            yield rx.toast(
                f"Speed limited to {max_limit} RPM by configuration.", duration=3000,
            )
        if self.target_speed != new_speed:
            logs = await self.get_state(LogState)
            logs.add_log("info", "Motor", f"Target speed set to {new_speed} RPM.")
        self.target_speed = new_speed

    @rx.event
    def set_bias(self, value: int):
        """Set the directional bias."""
        self.directional_bias = int(value)

    @rx.event
    async def toggle_motor(self):
        """Start or stop the motor normal operation."""
        if self.emergency_stop_active:
            yield rx.toast("Cannot start motor: Emergency Stop Active!", duration=3000)
            return
        logs = await self.get_state(LogState)
        self.is_motor_running = not self.is_motor_running
        if self.is_motor_running:
            logs.add_log("info", "Motor", "Motor sequence initiated manually.")
            yield rx.toast("Motor sequence initiated.", duration=2000)
        else:
            self.target_speed = 0
            logs.add_log("info", "Motor", "Motor stopped manually.")
            yield rx.toast("Motor stopped.", duration=2000)

    @rx.event
    def request_estop(self):
        """Show confirmation for E-Stop."""
        self.show_estop_confirm = True

    @rx.event
    def cancel_estop_request(self):
        """Cancel E-Stop confirmation."""
        self.show_estop_confirm = False

    @rx.event
    async def confirm_estop(self):
        """Trigger actual Emergency Stop."""
        self.emergency_stop_active = True
        self.is_motor_running = False
        self.target_speed = 0
        self.active_keys = {}
        self.show_estop_confirm = False
        logs = await self.get_state(LogState)
        logs.add_log(
            "error", "System", "EMERGENCY STOP TRIGGERED BY USER. SYSTEM HALTED.",
        )
        yield rx.toast("EMERGENCY STOP TRIGGERED! System Halted.", duration=5000)

    @rx.event
    async def reset_estop(self):
        """Reset the Emergency Stop state."""
        self.emergency_stop_active = False
        logs = await self.get_state(LogState)
        logs.add_log(
            "warning", "System", "Emergency stop reset. System returned to ready state.",
        )
        yield rx.toast("Emergency Stop reset. System ready.", duration=3000)