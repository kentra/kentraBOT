import reflex as rx
from app.pages.system_status import system_status_page
from app.pages.manual_control import manual_control_page
from app.pages.configuration import configuration_page
from app.pages.system_logs import system_logs_page
from app.pages.temp_page import test_page
app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
    ],
    style={"font_family": "Inter, sans-serif"},
)
app.add_page(system_status_page, route="/", title="System Status | RoboBelt")
app.add_page(manual_control_page, route="/manual", title="Manual Control | RoboBelt")
app.add_page(configuration_page, route="/config", title="Configuration | RoboBelt")
app.add_page(system_logs_page, route="/logs", title="System Logs | RoboBelt")
app.add_page(test_page, route="/temp_page", title="Testing testing | RoboBelt")