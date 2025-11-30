import reflex as rx


class ThemeState(rx.State):
    theme_mode: str = rx.LocalStorage("dark", name="theme_mode", sync=True)

    @rx.event
    def set_dark_mode(self):
        self.theme_mode = "dark"

    @rx.event
    def set_light_mode(self):
        self.theme_mode = "light"

    @rx.event
    def set_contrast_mode(self):
        self.theme_mode = "contrast"

    @rx.var
    def bg_color(self) -> str:
        if self.theme_mode == "light":
            return "#F9FAFB"
        if self.theme_mode == "contrast":
            return "#0A1026"
        return "#212B38"

    @rx.var
    def card_color(self) -> str:
        if self.theme_mode == "light":
            return "#FFFFFF"
        if self.theme_mode == "contrast":
            return "#0E1737"
        return "#37465B"

    @rx.var
    def text_primary(self) -> str:
        if self.theme_mode == "light":
            return "#111827"
        if self.theme_mode == "contrast":
            return "#FFFFFF"
        return "#FFFFFF"

    @rx.var
    def text_secondary(self) -> str:
        if self.theme_mode == "light":
            return "#6B7280"
        if self.theme_mode == "contrast":
            return "#9CA3AF"
        return "#9CA3AF"

    @rx.var
    def accent_color(self) -> str:
        if self.theme_mode == "light":
            return "#0D9488"
        if self.theme_mode == "contrast":
            return "#E37AFB"
        return "#08C6AB"

    @rx.var
    def border_color(self) -> str:
        if self.theme_mode == "light":
            return "#E5E7EB"
        if self.theme_mode == "contrast":
            return "#245879"
        return "#37465B"

    @rx.var
    def border_width(self) -> str:
        if self.theme_mode == "contrast":
            return "1px"
        return "1px"

    @rx.var
    def success_color(self) -> str:
        if self.theme_mode == "light":
            return "#059669"
        if self.theme_mode == "contrast":
            return "#08C6AB"
        return "#08C6AB"

    @rx.var
    def warning_color(self) -> str:
        if self.theme_mode == "light":
            return "#D97706"
        if self.theme_mode == "contrast":
            return "#F59E0B"
        return "#F59E0B"

    @rx.var
    def error_color(self) -> str:
        if self.theme_mode == "light":
            return "#DC2626"
        if self.theme_mode == "contrast":
            return "#EF4444"
        return "#EF4444"

    @rx.var
    def is_contrast(self) -> bool:
        return self.theme_mode == "contrast"
