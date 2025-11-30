import reflex as rx
from app.components.nav_item import nav_item
from app.states.ui_state import UIState
from app.states.theme_state import ThemeState


def theme_button(icon: str, mode: str, on_click: rx.event.EventType) -> rx.Component:
    is_active = ThemeState.theme_mode == mode
    return rx.el.button(
        rx.icon(icon, class_name="w-4 h-4"),
        on_click=on_click,
        class_name="p-2 rounded-md transition-colors",
        style=rx.cond(
            is_active,
            {
                "backgroundColor": ThemeState.accent_color,
                "color": rx.cond(ThemeState.is_contrast, "black", "white"),
                "border": rx.cond(ThemeState.is_contrast, "2px solid white", "none"),
            },
            {"color": ThemeState.text_secondary, "backgroundColor": "transparent"},
        ),
        title=f"Switch to {mode} theme",
    )


def sidebar() -> rx.Component:
    """The main left navigation sidebar."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("cpu", class_name="w-8 h-8 mr-3"),
                rx.el.h1(
                    "RoboBelt",
                    class_name="text-xl font-bold tracking-tight",
                    style={"color": ThemeState.text_primary},
                ),
                class_name="flex items-center px-6 py-6 border-b",
                style={
                    "color": ThemeState.accent_color,
                    "borderColor": ThemeState.border_color,
                    "borderBottomWidth": ThemeState.border_width,
                },
            ),
            rx.el.nav(
                rx.el.div(
                    rx.el.span(
                        "MAIN MENU",
                        class_name="text-xs font-semibold uppercase tracking-wider px-4 mb-2 block",
                        style={"color": ThemeState.text_secondary},
                    ),
                    nav_item("System Status", "layout-dashboard", "/"),
                    nav_item("Manual Control", "gamepad-2", "/manual"),
                    nav_item("Configuration", "settings-2", "/config"),
                    nav_item("System Logs", "file-text", "/logs"),
                    class_name="px-4 py-4 space-y-1",
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "THEME",
                        class_name="text-xs font-semibold mb-3 uppercase",
                        style={"color": ThemeState.text_secondary},
                    ),
                    rx.el.div(
                        theme_button("moon", "dark", ThemeState.set_dark_mode),
                        theme_button("sun", "light", ThemeState.set_light_mode),
                        theme_button(
                            "contrast", "contrast", ThemeState.set_contrast_mode
                        ),
                        class_name="flex gap-2 mb-6",
                    ),
                    class_name="px-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon("user", class_name="w-5 h-5"),
                        class_name="w-10 h-10 rounded-full flex items-center justify-center border",
                        style={
                            "backgroundColor": ThemeState.card_color,
                            "borderColor": ThemeState.border_color,
                            "color": ThemeState.text_secondary,
                        },
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Admin User",
                            class_name="text-sm font-medium",
                            style={"color": ThemeState.text_primary},
                        ),
                        rx.el.p(
                            "Online",
                            class_name="text-xs font-medium",
                            style={"color": ThemeState.accent_color},
                        ),
                        class_name="ml-3",
                    ),
                    class_name="flex items-center",
                ),
                class_name="p-4 border-t",
                style={
                    "borderColor": ThemeState.border_color,
                    "borderTopWidth": ThemeState.border_width,
                },
            ),
            class_name="flex flex-col h-full border-r shadow-xl transition-colors duration-300",
            style={
                "backgroundColor": ThemeState.card_color,
                "borderColor": ThemeState.border_color,
                "borderRightWidth": ThemeState.border_width,
            },
        ),
        class_name=rx.cond(
            UIState.is_mobile_menu_open,
            "fixed inset-y-0 left-0 z-50 w-64 transform transition-transform duration-300 ease-in-out translate-x-0",
            "hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0 z-30",
        ),
    )