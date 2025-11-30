import reflex as rx
from app.components.sidebar import sidebar
from app.components.status_panel import status_panel
from app.states.ui_state import UIState
from app.states.theme_state import ThemeState


def mobile_header(page_title: str) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("menu", class_name="w-6 h-6"),
            on_click=UIState.toggle_mobile_menu,
            class_name="md:hidden p-2 mr-2 rounded-md hover:bg-gray-700",
            style={"color": ThemeState.text_secondary},
        ),
        rx.el.h1(
            page_title,
            class_name="text-lg font-semibold truncate",
            style={"color": ThemeState.text_primary},
        ),
        class_name="flex items-center p-4 border-b md:hidden sticky top-0 z-20",
        style={
            "backgroundColor": ThemeState.card_color,
            "borderColor": ThemeState.border_color,
        },
    )


def main_layout(
    page_content: rx.Component, page_title: str = "Dashboard"
) -> rx.Component:
    """The main layout wrapper implementing the 3-column structure."""
    return rx.el.div(
        rx.cond(
            UIState.is_mobile_menu_open,
            rx.el.div(
                class_name="fixed inset-0 bg-black bg-opacity-75 z-40 transition-opacity md:hidden",
                on_click=UIState.close_mobile_menu,
            ),
            rx.fragment(),
        ),
        sidebar(),
        rx.el.div(
            mobile_header(page_title),
            rx.el.main(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            page_title,
                            class_name="text-2xl font-bold",
                            style={"color": ThemeState.text_primary},
                        ),
                        rx.el.p(
                            "Manage and monitor your robotic belt system.",
                            class_name="text-sm mt-1",
                            style={"color": ThemeState.text_secondary},
                        ),
                        class_name="hidden md:block mb-8",
                    ),
                    page_content,
                    class_name="max-w-5xl mx-auto w-full",
                ),
                class_name="flex-1 overflow-y-auto p-4 md:p-8",
            ),
            class_name="flex flex-col flex-1 md:pl-64 lg:pr-80 min-h-screen transition-all duration-300",
            style={"backgroundColor": ThemeState.bg_color},
        ),
        status_panel(),
        class_name="flex h-screen w-full font-sans overflow-hidden transition-colors duration-300",
        style={"backgroundColor": ThemeState.bg_color},
    )