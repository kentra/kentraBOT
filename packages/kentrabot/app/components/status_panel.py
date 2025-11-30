import reflex as rx
from app.states.ui_state import UIState
from app.states.telemetry_state import TelemetryState
from app.states.log_state import LogState, LogEntry
from app.states.theme_state import ThemeState


def log_item(entry: LogEntry) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            entry.timestamp,
            class_name="text-[10px] mb-1 block",
            style={"color": ThemeState.text_secondary},
        ),
        rx.el.p(
            entry.message,
            class_name="text-xs leading-snug",
            style={"color": ThemeState.text_primary},
        ),
        class_name="mb-3 pb-3 border-b last:border-0 last:mb-0 last:pb-0",
        style={
            "borderColor": ThemeState.border_color,
            "borderBottomWidth": ThemeState.border_width,
        },
    )


def status_panel_item(label: str, value: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            label, class_name="text-sm", style={"color": ThemeState.text_secondary},
        ),
        rx.el.span(
            value,
            class_name="text-sm font-medium",
            style={"color": ThemeState.text_primary},
        ),
        class_name="flex justify-between items-center py-2 border-b last:border-0",
        style={
            "borderColor": ThemeState.border_color,
            "borderBottomWidth": ThemeState.border_width,
        },
    )


def status_panel() -> rx.Component:
    """The right-side panel for quick status and logs summary."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Live Telemetry",
                    class_name="text-sm font-bold uppercase tracking-wider",
                    style={"color": ThemeState.text_primary},
                ),
                rx.el.div(
                    class_name=rx.match(
                        TelemetryState.system_health,
                        (
                            "Optimal",
                            "w-2 h-2 rounded-full animate-pulse shadow-[0_0_8px_rgba(34,197,94,0.6)]",
                        ),
                        (
                            "Warning",
                            "w-2 h-2 rounded-full animate-pulse shadow-[0_0_8px_rgba(234,179,8,0.6)]",
                        ),
                        "w-2 h-2 rounded-full animate-pulse shadow-[0_0_8px_rgba(239,68,68,0.6)]",
                    ),
                    style={
                        "backgroundColor": rx.match(
                            TelemetryState.system_health,
                            ("Optimal", ThemeState.success_color),
                            ("Warning", ThemeState.warning_color),
                            ThemeState.error_color,
                        ),
                    },
                ),
                class_name="flex items-center justify-between p-4 border-b",
                style={
                    "backgroundColor": ThemeState.card_color,
                    "borderColor": ThemeState.border_color,
                    "borderBottomWidth": ThemeState.border_width,
                },
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Motor Stats",
                        class_name="text-xs font-semibold mb-3 uppercase",
                        style={"color": ThemeState.accent_color},
                    ),
                    status_panel_item("Speed", f"{TelemetryState.belt_speed} RPM"),
                    status_panel_item("Temp", f"{TelemetryState.motor_temp}°C"),
                    status_panel_item(
                        "Current", f"{TelemetryState.current_draw:.1f} A",
                    ),
                    class_name="mb-6 p-4 rounded-xl shadow-sm transition-colors duration-300",
                    style={
                        "backgroundColor": ThemeState.card_color,
                        "border": f"{ThemeState.border_width} solid {ThemeState.border_color}",
                    },
                ),
                rx.el.div(
                    rx.el.h3(
                        "Recent Events",
                        class_name="text-xs font-semibold mb-3 uppercase",
                        style={"color": ThemeState.accent_color},
                    ),
                    rx.el.div(
                        rx.foreach(LogState.recent_logs, log_item),
                        class_name="p-4 rounded-xl shadow-sm transition-colors duration-300",
                        style={
                            "backgroundColor": ThemeState.card_color,
                            "border": f"{ThemeState.border_width} solid {ThemeState.border_color}",
                        },
                    ),
                ),
                class_name="p-4 overflow-y-auto flex-1",
            ),
            class_name="flex flex-col h-full border-l transition-colors duration-300",
            style={
                "backgroundColor": ThemeState.card_color,
                "borderColor": ThemeState.border_color,
                "borderLeftWidth": ThemeState.border_width,
            },
        ),
        class_name=rx.cond(
            UIState.is_right_panel_open,
            "hidden lg:flex lg:w-80 lg:flex-col lg:fixed lg:inset-y-0 lg:right-0 z-20 transition-colors duration-300",
            "hidden",
        ),
    )