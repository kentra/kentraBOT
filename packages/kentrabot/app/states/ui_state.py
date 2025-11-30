import reflex as rx


class UIState(rx.State):
    """State to handle UI responsiveness and interactions."""

    is_mobile_menu_open: bool = False
    is_right_panel_open: bool = True

    @rx.event
    def toggle_mobile_menu(self):
        self.is_mobile_menu_open = not self.is_mobile_menu_open

    @rx.event
    def close_mobile_menu(self):
        self.is_mobile_menu_open = False

    @rx.event
    def toggle_right_panel(self):
        self.is_right_panel_open = not self.is_right_panel_open