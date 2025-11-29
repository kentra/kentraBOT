import reflex as rx
import asyncio
import random


class TelemetryState(rx.State):
    """State to handle real-time telemetry simulation."""

    motor_temp: int = 42
    belt_speed: int = 0
    belt_tension: float = 450.0
    current_draw: float = 2.4
    system_health: str = "Optimal"
    previous_health: str = "Optimal"
    uptime_seconds: int = 45600
    _is_running: bool = False

    @rx.var
    def uptime_formatted(self) -> str:
        hours = self.uptime_seconds // 3600
        minutes = self.uptime_seconds % 3600 // 60
        return f"{hours}h {minutes}m"

    @rx.var
    def health_color(self) -> str:
        if self.system_health == "Optimal":
            return "text-green-600"
        elif self.system_health == "Warning":
            return "text-yellow-600"
        return "text-red-600"

    @rx.var
    def health_bg_color(self) -> str:
        if self.system_health == "Optimal":
            return "bg-green-500"
        elif self.system_health == "Warning":
            return "bg-yellow-500"
        return "bg-red-500"

    @rx.var
    def tension_pct(self) -> str:
        val = (self.belt_tension - 300) / 3.0
        return f"{max(0, min(100, val)):.1f}%"

    @rx.event
    def start_simulation(self):
        if not self._is_running:
            self._is_running = True
            return TelemetryState.update_telemetry

    @rx.event(background=True)
    async def update_telemetry(self):
        while True:
            async with self:
                if not self._is_running:
                    break
                from app.states.control_state import ControlState
                from app.states.log_state import LogState

                control = await self.get_state(ControlState)
                target = control.target_speed if control.is_motor_running else 0
                if self.belt_speed < target:
                    self.belt_speed = min(target, self.belt_speed + 15)
                elif self.belt_speed > target:
                    self.belt_speed = max(target, self.belt_speed - 25)
                if self.belt_speed > 0:
                    self.belt_speed = int(
                        max(0, self.belt_speed + random.randint(-2, 2))
                    )
                self.motor_temp = int(
                    max(20, min(95, self.motor_temp + random.randint(-1, 2)))
                )
                base_tension = 450 + self.belt_speed * 0.2
                self.belt_tension = max(
                    300, min(600, base_tension + random.uniform(-10, 10))
                )
                base_current = 1.0 + self.belt_speed * 0.01
                self.current_draw = max(
                    0.5, min(8.0, base_current + random.uniform(-0.1, 0.1))
                )
                self.uptime_seconds += 2
                if (
                    self.motor_temp > 85
                    or self.belt_tension > 580
                    or self.belt_tension < 320
                ):
                    self.system_health = "Critical"
                elif (
                    self.motor_temp > 70
                    or self.belt_tension > 550
                    or self.belt_tension < 350
                ):
                    self.system_health = "Warning"
                else:
                    self.system_health = "Optimal"
                if self.system_health != self.previous_health:
                    log_state = await self.get_state(LogState)
                    if self.system_health == "Critical":
                        log_state.add_log(
                            "error",
                            "System",
                            f"CRITICAL HEALTH ALERT: Motor {self.motor_temp}°C, Tension {self.belt_tension:.0f}N",
                        )
                    elif self.system_health == "Warning":
                        log_state.add_log(
                            "warning",
                            "System",
                            f"System warning detected. Parameters deviating from optimal.",
                        )
                    elif (
                        self.system_health == "Optimal"
                        and self.previous_health != "Optimal"
                    ):
                        log_state.add_log(
                            "success",
                            "System",
                            "System parameters stabilized. Health is Optimal.",
                        )
                    self.previous_health = self.system_health
            await asyncio.sleep(2)