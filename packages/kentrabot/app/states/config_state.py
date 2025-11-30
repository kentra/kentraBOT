import reflex as rx
import json
import logging
from typing import Optional
from pydantic import BaseModel
from app.states.log_state import LogState


class SystemConfig(BaseModel):
    max_speed: int = 500
    pid_p: float = 1.0
    pid_i: float = 0.1
    pid_d: float = 0.05
    calibration_offset: int = 0


class ConfigState(rx.State):
    config_json: str = rx.LocalStorage("{}", name="system_config", sync=True)
    max_speed: int = 500
    pid_p: float = 1.0
    pid_i: float = 0.1
    pid_d: float = 0.05
    calibration_offset: int = 0
    has_unsaved_changes: bool = False

    @rx.event
    def on_mount(self):
        """Load configuration from local storage on mount."""
        try:
            if self.config_json and self.config_json != "{}":
                data = json.loads(self.config_json)
                config = SystemConfig(**data)
                self.max_speed = config.max_speed
                self.pid_p = config.pid_p
                self.pid_i = config.pid_i
                self.pid_d = config.pid_d
                self.calibration_offset = config.calibration_offset
        except Exception as e:
            logging.exception(f"Error: {e}")
            print(f"Failed to load config: {e}")

    @rx.event
    def update_field(self, field: str, value: str):
        """Generic handler for form field updates to track unsaved changes."""
        self.has_unsaved_changes = True

    @rx.event
    def set_max_speed(self, value: str):
        try:
            self.max_speed = int(float(value))
            self.has_unsaved_changes = True
        except ValueError as e:
            logging.exception(f"Error: {e}")
            pass

    @rx.event
    def set_pid_p(self, value: str):
        try:
            self.pid_p = float(value)
            self.has_unsaved_changes = True
        except ValueError as e:
            logging.exception(f"Error: {e}")
            pass

    @rx.event
    def set_pid_i(self, value: str):
        try:
            self.pid_i = float(value)
            self.has_unsaved_changes = True
        except ValueError as e:
            logging.exception(f"Error: {e}")
            pass

    @rx.event
    def set_pid_d(self, value: str):
        try:
            self.pid_d = float(value)
            self.has_unsaved_changes = True
        except ValueError as e:
            logging.exception(f"Error: {e}")
            pass

    @rx.event
    def set_calibration_offset(self, value: str):
        try:
            self.calibration_offset = int(float(value))
            self.has_unsaved_changes = True
        except ValueError as e:
            logging.exception(f"Error: {e}")
            pass

    @rx.event
    async def save_config(self):
        """Save current state values to local storage."""
        try:
            if not 0 <= self.max_speed <= 1000:
                yield rx.toast("Max speed must be between 0 and 1000.", duration=3000)
                return
            if not -50 <= self.calibration_offset <= 50:
                yield rx.toast("Offset must be between -50 and 50.", duration=3000)
                return
            new_config = SystemConfig(
                max_speed=self.max_speed,
                pid_p=self.pid_p,
                pid_i=self.pid_i,
                pid_d=self.pid_d,
                calibration_offset=self.calibration_offset,
            )
            self.config_json = new_config.model_dump_json()
            self.has_unsaved_changes = False
            logs = await self.get_state(LogState)
            logs.add_log(
                "info", "Config", "Configuration updated and saved successfully."
            )
            yield rx.toast("Configuration saved successfully.", duration=3000)
        except Exception as e:
            logging.exception(f"Error: {e}")
            yield rx.toast(f"Error saving configuration: {str(e)}", duration=3000)

    @rx.event
    async def reset_defaults(self):
        """Reset form values to system defaults (does not auto-save)."""
        defaults = SystemConfig()
        self.max_speed = defaults.max_speed
        self.pid_p = defaults.pid_p
        self.pid_i = defaults.pid_i
        self.pid_d = defaults.pid_d
        self.calibration_offset = defaults.calibration_offset
        self.has_unsaved_changes = True
        logs = await self.get_state(LogState)
        logs.add_log(
            "warning", "Config", "Configuration values reset to defaults (unsaved)."
        )
        yield rx.toast("Values reset to defaults. Click Save to apply.", duration=3000)