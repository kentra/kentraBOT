import reflex as rx
from app.components.layout import main_layout
from app.states.control_state import ControlState
from app.states.theme_state import ThemeState


def key_button(
    label: str, key_code: str, icon: str = None, wide: bool = False
) -> rx.Component:
    """A visual keyboard key component."""
    is_pressed = ControlState.active_keys[key_code]
    return rx.el.button(
        rx.cond(
            icon,
            rx.icon(icon, class_name="w-6 h-6"),
            rx.el.span(label, class_name="text-xl font-bold"),
        ),
        on_mouse_down=lambda: ControlState.handle_key_down(key_code),
        on_mouse_up=lambda: ControlState.handle_key_up(key_code),
        on_mouse_leave=lambda: ControlState.handle_key_up(key_code),
        class_name=f"{('w-full' if wide else 'w-16')} h-16 rounded-lg border-2 flex items-center justify-center transition-all duration-75 select-none active:scale-95 hover:border-gray-500",
        style=rx.cond(
            is_pressed,
            {
                "backgroundColor": ThemeState.accent_color,
                "borderColor": ThemeState.accent_color,
                "color": rx.cond(ThemeState.is_contrast, "black", "#212B38"),
            },
            {
                "backgroundColor": "transparent",
                "borderColor": ThemeState.border_color,
                "color": ThemeState.text_secondary,
            },
        ),
    )


def drone_telemetry_item(label: str, value: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            label,
            class_name="text-xs font-medium uppercase tracking-wider",
            style={"color": ThemeState.text_secondary},
        ),
        rx.el.span(
            value,
            class_name="text-lg font-mono font-bold",
            style={"color": ThemeState.accent_color},
        ),
        class_name="flex flex-col p-3 rounded-lg border",
        style={
            "backgroundColor": ThemeState.bg_color,
            "borderColor": ThemeState.border_color,
            "borderWidth": ThemeState.border_width,
        },
    )


def webcam_feed() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    class_name=rx.cond(
                        ControlState.camera_connected,
                        "w-3 h-3 rounded-full bg-red-500 animate-pulse mr-2",
                        "hidden",
                    )
                ),
                rx.el.span(
                    rx.cond(ControlState.camera_connected, "LIVE", "OFFLINE"),
                    class_name="text-xs font-bold text-white tracking-wider",
                ),
                class_name="absolute top-4 left-4 bg-black/50 px-3 py-1 rounded-full flex items-center backdrop-blur-sm border border-white/10 z-10",
            ),
            rx.cond(
                ControlState.camera_connected,
                rx.el.div(
                    rx.icon(
                        "camera",
                        class_name="w-16 h-16 opacity-50 mb-4",
                        style={"color": ThemeState.accent_color},
                    ),
                    rx.el.p(
                        "Camera Feed Active",
                        class_name="font-mono",
                        style={"color": ThemeState.text_secondary},
                    ),
                    rx.el.p(
                        "Signal Strength: 98%",
                        class_name="text-xs mt-2",
                        style={"color": ThemeState.accent_color},
                    ),
                    class_name="absolute inset-0 flex flex-col items-center justify-center",
                    style={"backgroundColor": ThemeState.bg_color},
                ),
                rx.el.div(
                    rx.icon(
                        "video-off",
                        class_name="w-16 h-16 mb-4",
                        style={"color": ThemeState.text_secondary},
                    ),
                    rx.el.p(
                        "Camera Disconnected",
                        class_name="font-medium",
                        style={"color": ThemeState.text_secondary},
                    ),
                    class_name="absolute inset-0 flex flex-col items-center justify-center",
                    style={"backgroundColor": ThemeState.card_color},
                ),
            ),
            rx.el.div(
                rx.el.div(
                    class_name="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 border border-white/30 rounded-full"
                ),
                rx.el.div(
                    class_name="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-1 h-1 rounded-full",
                    style={"backgroundColor": ThemeState.accent_color},
                ),
                rx.el.div(
                    class_name="absolute top-1/2 left-0 right-0 h-[1px] bg-white/10"
                ),
                rx.el.div(
                    class_name="absolute left-1/2 top-0 bottom-0 w-[1px] bg-white/10"
                ),
                class_name="absolute inset-0 pointer-events-none",
            ),
            class_name="relative w-full aspect-video bg-black rounded-lg overflow-hidden shadow-lg border",
            style={
                "borderColor": ThemeState.border_color,
                "borderWidth": ThemeState.border_width,
            },
        ),
        rx.el.div(
            rx.el.button(
                rx.cond(
                    ControlState.camera_connected,
                    "Disconnect Camera",
                    "Connect Camera stream",
                ),
                on_click=ControlState.toggle_camera,
                class_name=rx.cond(
                    ControlState.camera_connected,
                    "text-xs text-red-400 hover:text-red-300 transition-colors",
                    "text-xs hover:opacity-80 transition-colors",
                ),
                style=rx.cond(
                    ControlState.camera_connected,
                    {},
                    {"color": ThemeState.accent_color},
                ),
            ),
            rx.el.span(
                ControlState.connection_status_text,
                class_name="text-xs ml-auto font-medium",
                style={
                    "color": rx.cond(
                        ControlState.camera_connected,
                        ThemeState.success_color,
                        ThemeState.error_color,
                    )
                },
            ),
            class_name="flex justify-between items-center mt-3 px-1",
        ),
        class_name="flex flex-col h-full",
    )


def estop_modal() -> rx.Component:
    return rx.cond(
        ControlState.show_estop_confirm,
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "CONFIRM EMERGENCY STOP",
                    class_name="text-lg font-bold text-red-500 mb-2",
                ),
                rx.el.p(
                    "Are you sure you want to trigger the emergency stop? This will immediately halt all system operations.",
                    class_name="mb-6",
                    style={"color": ThemeState.text_secondary},
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=ControlState.cancel_estop_request,
                        class_name="px-4 py-2 rounded-lg font-medium mr-3",
                        style={
                            "backgroundColor": "transparent",
                            "color": ThemeState.text_primary,
                            "border": f"1px solid {ThemeState.border_color}",
                        },
                    ),
                    rx.el.button(
                        "TRIGGER STOP",
                        on_click=ControlState.confirm_estop,
                        class_name="px-4 py-2 bg-red-600 text-white rounded-lg font-bold hover:bg-red-700 shadow-lg",
                    ),
                    class_name="flex justify-end",
                ),
                class_name="p-6 rounded-xl shadow-2xl max-w-md w-full mx-4 z-50 animate-in fade-in zoom-in duration-200",
                style={
                    "backgroundColor": ThemeState.card_color,
                    "border": f"{ThemeState.border_width} solid {ThemeState.border_color}",
                },
            ),
            class_name="fixed inset-0 bg-black/70 z-50 flex items-center justify-center",
        ),
        rx.fragment(),
    )


def estop_overlay() -> rx.Component:
    return rx.cond(
        ControlState.emergency_stop_active,
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "flag_triangle_right", class_name="w-24 h-24 text-red-500 mb-6"
                ),
                rx.el.h3(
                    "SYSTEM HALTED",
                    class_name="text-4xl font-black text-red-500 mb-4 tracking-widest",
                ),
                rx.el.p(
                    "EMERGENCY STOP ACTIVE",
                    class_name="text-xl text-white font-bold mb-8",
                ),
                rx.el.button(
                    "RESET SYSTEM",
                    on_click=ControlState.reset_estop,
                    class_name="px-8 py-4 bg-red-600 text-white font-bold rounded-xl hover:bg-red-700 transition-all hover:scale-105 shadow-[0_0_30px_rgba(220,38,38,0.5)]",
                ),
                class_name="flex flex-col items-center justify-center z-40",
            ),
            class_name="absolute inset-0 backdrop-blur-sm flex items-center justify-center rounded-xl border-2 border-red-500/50",
            style={"backgroundColor": "rgba(0,0,0,0.9)"},
        ),
        rx.fragment(),
    )


def manual_control_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            estop_modal(),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Visual Feed",
                        class_name="text-lg font-semibold mb-4 flex items-center gap-2",
                        style={"color": ThemeState.text_primary},
                    ),
                    rx.el.div(
                        webcam_feed(),
                        class_name="p-4 rounded-xl shadow-sm h-fit",
                        style={
                            "backgroundColor": ThemeState.card_color,
                            "border": f"{ThemeState.border_width} solid {ThemeState.border_color}",
                        },
                    ),
                    rx.el.div(
                        drone_telemetry_item(
                            "Altitude", f"{ControlState.drone_altitude:.1f}m"
                        ),
                        drone_telemetry_item(
                            "Speed", f"{ControlState.target_speed} RPM"
                        ),
                        drone_telemetry_item(
                            "Heading", f"{ControlState.drone_heading}°"
                        ),
                        class_name="grid grid-cols-3 gap-4 mt-4",
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Command Interface",
                        class_name="text-lg font-semibold mb-4",
                        style={"color": ThemeState.text_primary},
                    ),
                    rx.el.div(
                        estop_overlay(),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "ALTITUDE",
                                    class_name="text-xs font-bold mb-2 text-center",
                                    style={"color": ThemeState.text_secondary},
                                ),
                                rx.el.div(
                                    key_button("W", "w", "arrow-big-up"),
                                    class_name="flex justify-center mb-2",
                                ),
                                rx.el.div(
                                    key_button("S", "s", "arrow-big-down"),
                                    class_name="flex justify-center",
                                ),
                                class_name="mr-8",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "NAVIGATION",
                                    class_name="text-xs font-bold mb-2 text-center",
                                    style={"color": ThemeState.text_secondary},
                                ),
                                rx.el.div(
                                    key_button("UP", "arrowup", "arrow-up"),
                                    class_name="flex justify-center mb-2",
                                ),
                                rx.el.div(
                                    key_button("LEFT", "arrowleft", "arrow-left"),
                                    key_button("DOWN", "arrowdown", "arrow-down"),
                                    key_button("RIGHT", "arrowright", "arrow-right"),
                                    class_name="flex gap-2",
                                ),
                                class_name="flex flex-col",
                            ),
                            class_name="flex items-center justify-center py-8",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "EMERGENCY STOP",
                                on_click=ControlState.request_estop,
                                class_name="w-full py-4 bg-red-600 text-white font-bold rounded-xl hover:bg-red-700 shadow-lg transition-all active:scale-95 flex items-center justify-center gap-2",
                            ),
                            class_name="mt-auto border-t pt-6",
                            style={
                                "borderColor": ThemeState.border_color,
                                "borderTopWidth": ThemeState.border_width,
                            },
                        ),
                        class_name="p-6 rounded-xl shadow-sm h-full relative overflow-hidden flex flex-col",
                        style={
                            "backgroundColor": ThemeState.card_color,
                            "border": f"{ThemeState.border_width} solid {ThemeState.border_color}",
                        },
                    ),
                    class_name="flex flex-col",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
            ),
            class_name="outline-none focus:ring-0",
        ),
        page_title="Manual Control",
    )