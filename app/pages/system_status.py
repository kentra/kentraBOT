import reflex as rx
from app.components.layout import main_layout
from app.states.telemetry_state import TelemetryState
from app.states.theme_state import ThemeState
from app.components.visualizations import (
    temp_gauge,
    tension_meter,
    system_health_indicator,
)


def status_card(
    title: str, value: str, icon: str, trend: str = None, trend_up: bool = True
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    title,
                    class_name="text-sm font-medium",
                    style={"color": ThemeState.text_secondary},
                ),
                rx.el.h3(
                    value,
                    class_name="text-2xl font-bold mt-1",
                    style={"color": ThemeState.text_primary},
                ),
            ),
            rx.el.div(
                rx.icon(
                    icon, class_name="w-6 h-6", style={"color": ThemeState.accent_color}
                ),
                class_name="p-3 rounded-lg transition-colors duration-300",
                style={"backgroundColor": ThemeState.bg_color},
            ),
            class_name="flex justify-between items-start",
        ),
        rx.cond(
            trend != None,
            rx.el.div(
                rx.el.span(
                    trend,
                    class_name="text-xs font-medium flex items-center mt-4",
                    style={
                        "color": rx.cond(
                            trend_up, ThemeState.accent_color, ThemeState.error_color
                        )
                    },
                ),
                rx.el.span(
                    "vs last hour",
                    class_name="text-xs ml-2 mt-4",
                    style={"color": ThemeState.text_secondary},
                ),
                class_name="flex items-center",
            ),
            rx.el.div(class_name="mt-4 h-4"),
        ),
        class_name="p-6 rounded-xl transition-colors duration-300 hover:shadow-md",
        style={
            "backgroundColor": ThemeState.card_color,
            "border": f"{ThemeState.border_width} solid {ThemeState.border_color}",
        },
    )


def system_status_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.el.div(
                status_card(
                    "Belt Speed",
                    f"{TelemetryState.belt_speed} RPM",
                    "gauge",
                    "+2% Efficiency",
                    True,
                ),
                status_card(
                    "Motor Temp",
                    f"{TelemetryState.motor_temp}°C",
                    "thermometer",
                    "Optimal Range",
                    True,
                ),
                status_card(
                    "Power Draw",
                    f"{TelemetryState.current_draw:.1f} A",
                    "zap",
                    "-1.2% Usage",
                    True,
                ),
                status_card("Uptime", TelemetryState.uptime_formatted, "clock"),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "System Health & Diagnostics",
                            class_name="text-lg font-semibold",
                            style={"color": ThemeState.text_primary},
                        ),
                        system_health_indicator(),
                        class_name="flex justify-between items-center mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h4(
                                "Motor Thermal Monitor",
                                class_name="text-sm font-medium mb-6",
                                style={"color": ThemeState.text_secondary},
                            ),
                            temp_gauge(),
                            class_name="flex flex-col items-center justify-center p-6 rounded-xl transition-colors duration-300",
                            style={
                                "backgroundColor": ThemeState.bg_color,
                                "border": f"{ThemeState.border_width} solid {ThemeState.border_color}",
                            },
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.h4(
                                    "Belt Tension Analysis",
                                    class_name="text-sm font-medium mb-4",
                                    style={"color": ThemeState.text_secondary},
                                ),
                                tension_meter(),
                                class_name="mb-8",
                            ),
                            rx.el.div(
                                rx.el.h4(
                                    "Component Status",
                                    class_name="text-sm font-medium mb-3",
                                    style={"color": ThemeState.text_secondary},
                                ),
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.span(
                                            "Drive Motor",
                                            class_name="text-sm",
                                            style={"color": ThemeState.text_primary},
                                        ),
                                        rx.el.span(
                                            "Active",
                                            class_name="text-xs font-bold px-2 py-1 rounded-full",
                                            style={
                                                "color": ThemeState.success_color,
                                                "backgroundColor": rx.cond(
                                                    ThemeState.is_contrast,
                                                    "transparent",
                                                    "rgba(8, 198, 171, 0.2)",
                                                ),
                                                "border": rx.cond(
                                                    ThemeState.is_contrast,
                                                    f"1px solid {ThemeState.success_color}",
                                                    "none",
                                                ),
                                            },
                                        ),
                                        class_name="flex justify-between items-center py-2 border-b",
                                        style={
                                            "borderColor": ThemeState.border_color,
                                            "borderBottomWidth": ThemeState.border_width,
                                        },
                                    ),
                                    rx.el.div(
                                        rx.el.span(
                                            "Tensioner Arm",
                                            class_name="text-sm",
                                            style={"color": ThemeState.text_primary},
                                        ),
                                        rx.el.span(
                                            "Locked",
                                            class_name="text-xs font-bold px-2 py-1 rounded-full",
                                            style={
                                                "color": ThemeState.success_color,
                                                "backgroundColor": rx.cond(
                                                    ThemeState.is_contrast,
                                                    "transparent",
                                                    "rgba(8, 198, 171, 0.2)",
                                                ),
                                                "border": rx.cond(
                                                    ThemeState.is_contrast,
                                                    f"1px solid {ThemeState.success_color}",
                                                    "none",
                                                ),
                                            },
                                        ),
                                        class_name="flex justify-between items-center py-2 border-b",
                                        style={
                                            "borderColor": ThemeState.border_color,
                                            "borderBottomWidth": ThemeState.border_width,
                                        },
                                    ),
                                    rx.el.div(
                                        rx.el.span(
                                            "Emergency Stop",
                                            class_name="text-sm",
                                            style={"color": ThemeState.text_primary},
                                        ),
                                        rx.el.span(
                                            "Disengaged",
                                            class_name="text-xs font-bold px-2 py-1 rounded-full",
                                            style={
                                                "color": ThemeState.text_secondary,
                                                "backgroundColor": ThemeState.bg_color,
                                                "border": f"{ThemeState.border_width} solid {ThemeState.border_color}",
                                            },
                                        ),
                                        class_name="flex justify-between items-center py-2",
                                    ),
                                    class_name="rounded-xl p-4",
                                    style={
                                        "backgroundColor": ThemeState.card_color,
                                        "border": f"{ThemeState.border_width} solid {ThemeState.border_color}",
                                    },
                                ),
                            ),
                            class_name="flex flex-col justify-center",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-8",
                    ),
                    class_name="p-6 rounded-xl shadow-sm transition-colors duration-300",
                    style={
                        "backgroundColor": ThemeState.card_color,
                        "border": f"{ThemeState.border_width} solid {ThemeState.border_color}",
                    },
                ),
                class_name="mb-8",
            ),
            class_name="flex flex-col",
            on_mount=TelemetryState.start_simulation,
        ),
        page_title="System Status",
    )