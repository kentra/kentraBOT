import reflex as rx
from app.states.theme_state import ThemeState


def nav_item(text: str, icon_name: str, url: str) -> rx.Component:
    """A navigation item component for the sidebar."""
    return rx.el.a(
        rx.el.div(
            rx.icon(
                icon_name,
                class_name="w-5 h-5 mr-3 transition-colors",
                style={"color": ThemeState.text_secondary},
            ),
            rx.el.span(
                text,
                class_name="font-medium transition-colors",
                style={"color": ThemeState.text_secondary},
            ),
            class_name="flex items-center px-4 py-3 rounded-lg group transition-all duration-200 cursor-pointer hover:bg-gray-100/10",
            style={"borderColor": "transparent"},
        ),
        href=url,
        class_name="block mb-1",
    )