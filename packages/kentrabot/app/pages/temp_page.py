import reflex as rx
from app.components.layout import main_layout

def test_page() -> rx.Component:
    return main_layout(rx.el.div(), page_title="Testing Page",)