import reflex as rx
from datetime import datetime


class LogEntry(rx.Base):
    id: int
    timestamp: str
    severity: str
    category: str
    message: str


class LogState(rx.State):
    entries: list[LogEntry] = []
    filter_mode: str = "All"
    _next_id: int = 0

    @rx.event
    def on_mount(self):
        """Initialize with some default logs if empty."""
        if not self.entries:
            self.add_log("info", "System", "System initialized successfully.")
            self.add_log("success", "Network", "Connection established with PLC.")

    @rx.event
    def add_log(self, severity: str, category: str, message: str):
        """Add a new log entry. This can be called from other states."""
        now = datetime.now().strftime("%H:%M:%S")
        entry = LogEntry(
            id=self._next_id,
            timestamp=now,
            severity=severity,
            category=category,
            message=message,
        )
        self.entries.insert(0, entry)
        self._next_id += 1
        if len(self.entries) > 100:
            self.entries.pop()

    @rx.event
    def set_filter(self, mode: str):
        self.filter_mode = mode

    @rx.event
    def clear_logs(self):
        self.entries = []

    @rx.var
    def filtered_entries(self) -> list[LogEntry]:
        if self.filter_mode == "All":
            return self.entries
        elif self.filter_mode == "Errors Only":
            return [e for e in self.entries if e.severity == "error"]
        elif self.filter_mode == "Warnings":
            return [e for e in self.entries if e.severity == "warning"]
        elif self.filter_mode == "System Events":
            return [e for e in self.entries if e.category == "System"]
        return self.entries

    @rx.var
    def recent_logs(self) -> list[LogEntry]:
        """Return the 5 most recent logs for the dashboard panel."""
        return self.entries[:5]