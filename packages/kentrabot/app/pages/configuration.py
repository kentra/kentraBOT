import reflex as rx
from app.components.layout import main_layout
from app.states.config_state import ConfigState
from app.states.theme_state import ThemeState


def form_field(label: str, helper: str, input_component: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-sm font-medium mb-1",
            style={"color": ThemeState.text_primary},
        ),
        input_component,
        rx.el.p(
            helper,
            class_name="text-xs mt-1",
            style={"color": ThemeState.text_secondary},
        ),
        class_name="mb-5",
    )


def configuration_page() -> rx.Component:
    input_style = {
        "backgroundColor": ThemeState.bg_color,
        "borderColor": ThemeState.border_color,
        "color": ThemeState.text_primary,
        "borderWidth": ThemeState.border_width,
    }
    return main_layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "System Parameters",
                        class_name="text-lg font-semibold",
                        style={"color": ThemeState.text_primary},
                    ),
                    rx.cond(
                        ConfigState.has_unsaved_changes,
                        rx.el.span(
                            "Unsaved Changes",
                            class_name="px-3 py-1 text-xs font-bold rounded-full animate-pulse",
                            style={
                                "color": ThemeState.warning_color,
                                "backgroundColor": rx.cond(
                                    ThemeState.is_contrast,
                                    "transparent",
                                    "rgba(245, 158, 11, 0.1)",
                                ),
                                "border": rx.cond(
                                    ThemeState.is_contrast,
                                    f"1px solid {ThemeState.warning_color}",
                                    "none",
                                ),
                            },
                        ),
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Motion Limits",
                            class_name="text-sm font-bold uppercase tracking-wider mb-4",
                            style={"color": ThemeState.accent_color},
                        ),
                        form_field(
                            "Maximum Speed Limit (RPM)",
                            "Hard limit for motor controller. Max: 1000 RPM.",
                            rx.el.input(
                                type="number",
                                on_change=ConfigState.set_max_speed,
                                class_name="w-full px-4 py-2 rounded-lg outline-none transition-all border focus:ring-1 focus:ring-current",
                                style=input_style,
                                default_value=ConfigState.max_speed,
                            ),
                        ),
                        form_field(
                            "Calibration Offset",
                            "Zero-point adjustment for belt centering (-50 to +50).",
                            rx.el.input(
                                type="number",
                                on_change=ConfigState.set_calibration_offset,
                                class_name="w-full px-4 py-2 rounded-lg outline-none transition-all border focus:ring-1 focus:ring-current",
                                style=input_style,
                                default_value=ConfigState.calibration_offset.to_string(),
                            ),
                        ),
                        class_name="md:col-span-1",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "PID Control Tuning",
                            class_name="text-sm font-bold uppercase tracking-wider mb-4",
                            style={"color": ThemeState.accent_color},
                        ),
                        rx.el.div(
                            form_field(
                                "Proportional (Kp)",
                                "Response to current error.",
                                rx.el.input(
                                    type="number",
                                    step="0.1",
                                    on_change=ConfigState.set_pid_p,
                                    class_name="w-full px-4 py-2 rounded-lg outline-none transition-all border focus:ring-1 focus:ring-current",
                                    style=input_style,
                                    default_value=ConfigState.pid_p.to_string(),
                                ),
                            ),
                            form_field(
                                "Integral (Ki)",
                                "Accumulated past errors.",
                                rx.el.input(
                                    type="number",
                                    step="0.01",
                                    on_change=ConfigState.set_pid_i,
                                    class_name="w-full px-4 py-2 rounded-lg outline-none transition-all border focus:ring-1 focus:ring-current",
                                    style=input_style,
                                    default_value=ConfigState.pid_i.to_string(),
                                ),
                            ),
                            form_field(
                                "Derivative (Kd)",
                                "Prediction of future errors.",
                                rx.el.input(
                                    type="number",
                                    step="0.01",
                                    on_change=ConfigState.set_pid_d,
                                    class_name="w-full px-4 py-2 rounded-lg outline-none transition-all border focus:ring-1 focus:ring-current",
                                    style=input_style,
                                    default_value=ConfigState.pid_d.to_string(),
                                ),
                            ),
                            class_name="grid grid-cols-3 gap-4",
                        ),
                        class_name="md:col-span-1",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-12",
                ),
                rx.el.div(
                    rx.el.hr(
                        class_name="my-8",
                        style={
                            "borderColor": ThemeState.border_color,
                            "borderTopWidth": ThemeState.border_width,
                        },
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Reset Defaults",
                            on_click=ConfigState.reset_defaults,
                            class_name="px-6 py-2.5 font-medium rounded-lg transition-colors",
                            style={
                                "backgroundColor": "transparent",
                                "color": ThemeState.text_primary,
                                "border": f"1px solid {ThemeState.border_color}",
                            },
                        ),
                        rx.el.button(
                            "Save Configuration",
                            on_click=ConfigState.save_config,
                            class_name="px-6 py-2.5 font-bold rounded-lg transition-all hover:shadow-lg active:scale-95",
                            style={
                                "backgroundColor": ThemeState.accent_color,
                                "color": rx.cond(
                                    ThemeState.is_contrast, "black", "#212B38"
                                ),
                                "border": rx.cond(
                                    ThemeState.is_contrast, "2px solid white", "none"
                                ),
                            },
                        ),
                        class_name="flex justify-between items-center",
                    ),
                ),
                class_name="p-8 rounded-xl shadow-sm",
                style={
                    "backgroundColor": ThemeState.card_color,
                    "border": f"{ThemeState.border_width} solid {ThemeState.border_color}",
                },
            ),
            class_name="space-y-6 max-w-4xl mx-auto",
            on_mount=ConfigState.on_mount,
        ),
        page_title="Configuration",
    )