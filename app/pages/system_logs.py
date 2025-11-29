import reflex as rx
from app.components.layout import main_layout
from app.states.log_state import LogState, LogEntry
from app.states.theme_state import ThemeState


def filter_button(label: str) -> rx.Component:
    is_active = LogState.filter_mode == label
    return rx.el.button(
        label,
        on_click=lambda: LogState.set_filter(label),
        class_name="px-4 py-2 font-medium rounded-lg transition-all shadow-sm",
        style=rx.cond(
            is_active,
            {
                "backgroundColor": ThemeState.accent_color,
                "color": rx.cond(ThemeState.is_contrast, "black", "#212B38"),
                "fontWeight": "bold",
            },
            {
                "backgroundColor": "transparent",
                "color": ThemeState.text_secondary,
                "border": f"1px solid {ThemeState.border_color}",
            },
        ),
    )


def log_row(entry: LogEntry) -> rx.Component:
    severity_base_style = {
        "fontWeight": "bold",
        "padding": "2px 8px",
        "borderRadius": "9999px",
        "display": "inline-block",
        "width": "5rem",
        "textAlign": "center",
        "fontSize": "0.75rem",
    }
    return rx.el.tr(
        rx.el.td(
            rx.el.span(entry.timestamp, class_name="font-mono text-sm opacity-70"),
            class_name="px-6 py-4 whitespace-nowrap",
            style={"color": ThemeState.text_secondary},
        ),
        rx.el.td(
            rx.el.span(
                entry.severity.upper(),
                style=rx.match(
                    entry.severity,
                    (
                        "error",
                        {
                            **severity_base_style,
                            "color": ThemeState.error_color,
                            "backgroundColor": "rgba(239, 68, 68, 0.1)",
                            "border": f"1px solid {ThemeState.error_color}",
                        },
                    ),
                    (
                        "warning",
                        {
                            **severity_base_style,
                            "color": ThemeState.warning_color,
                            "backgroundColor": "rgba(245, 158, 11, 0.1)",
                            "border": f"1px solid {ThemeState.warning_color}",
                        },
                    ),
                    (
                        "success",
                        {
                            **severity_base_style,
                            "color": ThemeState.success_color,
                            "backgroundColor": "rgba(16, 185, 129, 0.1)",
                            "border": f"1px solid {ThemeState.success_color}",
                        },
                    ),
                    {
                        **severity_base_style,
                        "color": ThemeState.accent_color,
                        "backgroundColor": "rgba(59, 130, 246, 0.1)",
                        "border": f"1px solid {ThemeState.accent_color}",
                    },
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                entry.category,
                class_name="text-sm font-medium",
                style={"color": ThemeState.text_secondary},
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.p(
                entry.message,
                class_name="text-sm",
                style={"color": ThemeState.text_primary},
            ),
            class_name="px-6 py-4",
        ),
        class_name="transition-colors border-b",
        style={
            "borderColor": ThemeState.border_color,
            "borderBottomWidth": ThemeState.border_width,
        },
    )


def system_logs_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "System Logs",
                        class_name="text-lg font-semibold",
                        style={"color": ThemeState.text_primary},
                    ),
                    rx.el.div(
                        rx.el.span(
                            f"{LogState.filtered_entries.length()} entries",
                            class_name="text-sm",
                            style={"color": ThemeState.text_secondary},
                        ),
                        rx.el.button(
                            rx.icon(
                                "trash-2",
                                class_name="w-4 h-4 hover:text-red-500",
                                style={"color": ThemeState.text_secondary},
                            ),
                            on_click=LogState.clear_logs,
                            class_name="ml-4 p-2 rounded-lg transition-colors hover:bg-gray-100/10",
                            title="Clear Logs",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    filter_button("All"),
                    filter_button("Errors Only"),
                    filter_button("Warnings"),
                    filter_button("System Events"),
                    class_name="flex flex-wrap gap-2 mb-6",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Timestamp",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Severity",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Category",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Message",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider",
                                ),
                            ),
                            style={
                                "backgroundColor": ThemeState.bg_color,
                                "color": ThemeState.text_secondary,
                                "borderBottom": f"{ThemeState.border_width} solid {ThemeState.border_color}",
                            },
                        ),
                        rx.el.tbody(rx.foreach(LogState.filtered_entries, log_row)),
                        class_name="min-w-full",
                    ),
                    class_name="overflow-x-auto rounded-xl border",
                    style={
                        "borderColor": ThemeState.border_color,
                        "borderWidth": ThemeState.border_width,
                    },
                ),
                class_name="p-6 rounded-xl shadow-sm",
                style={
                    "backgroundColor": ThemeState.card_color,
                    "border": f"{ThemeState.border_width} solid {ThemeState.border_color}",
                },
            ),
            class_name="space-y-6",
            on_mount=LogState.on_mount,
        ),
        page_title="System Logs",
    )