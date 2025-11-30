import reflex as rx
from app.states.telemetry_state import TelemetryState
from app.states.theme_state import ThemeState


def circular_gauge(
    value: int, max_val: int, label: str, unit: str, color_hex: str
) -> rx.Component:
    """A reusable circular gauge component using SVG."""
    radius = 36
    circumference = 2 * 3.14159 * radius
    offset_var = circumference * (1 - value / max_val)
    return rx.el.div(
        rx.el.div(
            rx.el.svg(
                rx.el.circle(
                    cx="50",
                    cy="50",
                    r=radius,
                    fill="none",
                    stroke=ThemeState.border_color,
                    stroke_width="8",
                ),
                rx.el.circle(
                    cx="50",
                    cy="50",
                    r=radius,
                    fill="none",
                    stroke=color_hex,
                    stroke_width="8",
                    stroke_dasharray=f"{circumference}",
                    stroke_dashoffset=offset_var,
                    stroke_linecap="round",
                    class_name="transition-all duration-1000 ease-out -rotate-90 origin-center",
                ),
                view_box="0 0 100 100",
                class_name="w-32 h-32",
            ),
            class_name="relative flex items-center justify-center",
        ),
        rx.el.div(
            rx.el.span(
                value,
                class_name="text-3xl font-bold",
                style={"color": ThemeState.text_primary},
            ),
            rx.el.span(
                unit,
                class_name="text-sm ml-1 mb-1",
                style={"color": ThemeState.text_secondary},
            ),
            class_name="absolute inset-0 flex items-center justify-center",
        ),
        rx.el.p(
            label,
            class_name="text-sm font-medium mt-2 text-center",
            style={"color": ThemeState.text_secondary},
        ),
        class_name="flex flex-col items-center relative",
    )


def temp_gauge() -> rx.Component:
    return circular_gauge(
        TelemetryState.motor_temp,
        100,
        "Motor Temp",
        "°C",
        rx.cond(
            TelemetryState.motor_temp > 80,
            ThemeState.error_color,
            rx.cond(
                TelemetryState.motor_temp > 60,
                ThemeState.warning_color,
                ThemeState.accent_color,
            ),
        ),
    )


def tension_meter() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                "Belt Tension",
                class_name="text-sm font-medium",
                style={"color": ThemeState.text_secondary},
            ),
            rx.el.span(
                rx.el.span(TelemetryState.belt_tension.to_string()),
                " N",
                class_name="text-lg font-bold",
                style={"color": ThemeState.text_primary},
            ),
            class_name="flex justify-between items-end mb-2",
        ),
        rx.el.div(
            rx.el.div(
                class_name="absolute inset-0 rounded-full border transition-colors duration-300",
                style={
                    "backgroundColor": ThemeState.bg_color,
                    "borderColor": ThemeState.border_color,
                },
            ),
            rx.el.div(
                class_name="absolute top-0 bottom-0 opacity-30 transition-colors duration-300",
                style={
                    "left": "33%",
                    "width": "50%",
                    "backgroundColor": ThemeState.accent_color,
                },
            ),
            rx.el.div(
                class_name="absolute top-0 bottom-0 rounded-full transition-all duration-500 shadow-sm",
                style={
                    "width": TelemetryState.tension_pct,
                    "backgroundColor": rx.cond(
                        (TelemetryState.belt_tension < 400)
                        | (TelemetryState.belt_tension > 550),
                        ThemeState.error_color,
                        ThemeState.accent_color,
                    ),
                },
            ),
            class_name="relative h-4 w-full rounded-full overflow-hidden inner-shadow",
        ),
        rx.el.div(
            rx.el.span(
                "300N", class_name="text-xs", style={"color": ThemeState.text_secondary}
            ),
            rx.el.span(
                "Optimal Range (400-550N)",
                class_name="text-xs font-medium",
                style={"color": ThemeState.accent_color},
            ),
            rx.el.span(
                "600N", class_name="text-xs", style={"color": ThemeState.text_secondary}
            ),
            class_name="flex justify-between mt-1",
        ),
        class_name="w-full p-4 rounded-xl shadow-sm transition-colors duration-300",
        style={
            "backgroundColor": ThemeState.card_color,
            "border": f"{ThemeState.border_width} solid {ThemeState.border_color}",
        },
    )


def system_health_indicator() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="w-3 h-3 rounded-full animate-pulse mr-2",
            style={
                "backgroundColor": rx.match(
                    TelemetryState.system_health,
                    ("Optimal", ThemeState.success_color),
                    ("Warning", ThemeState.warning_color),
                    ThemeState.error_color,
                )
            },
        ),
        rx.el.span(
            "System Status: ",
            class_name="text-sm mr-1",
            style={"color": ThemeState.text_secondary},
        ),
        rx.el.span(
            TelemetryState.system_health,
            class_name="text-sm font-bold",
            style={
                "color": rx.match(
                    TelemetryState.system_health,
                    ("Optimal", ThemeState.success_color),
                    ("Warning", ThemeState.warning_color),
                    ThemeState.error_color,
                )
            },
        ),
        class_name="flex items-center px-4 py-2 rounded-full shadow-sm transition-colors duration-300",
        style={"backgroundColor": ThemeState.card_color},
    )