"""Visual theme constants, ttk styles, and DateEntrySpinbox composite widget."""

import calendar
from datetime import date
import tkinter as tk
from tkinter import ttk

# Color palette
BG_PRIMARY = "#0F1E2E"
BG_SECONDARY = "#162A40"
BG_CARD = "#1C3550"
BG_INPUT = "#112233"
FG_PRIMARY = "#F0F6FC"
FG_SECONDARY = "#9FB3C8"
ACCENT_CYAN = "#17A2B8"
ACCENT_GREEN = "#198754"
ACCENT_RED = "#DC3545"
ACCENT_AMBER = "#E08E0B"
ACCENT_SLATE = "#3B536E"
BORDER_COLOR = "#284B6E"
FONT_FAMILY = "DejaVu Sans"

LOGIN_WINDOW_TITLE = "Login - Compensándote"
MAIN_WINDOW_TITLE = "Caja Compensándote – Control de Afiliados"
ABOUT_WINDOW_TITLE = "Acerca de - Compensándote"


def apply_theme(root: tk.Misc) -> None:
    """Applies the dark-cyan visual style to Tkinter/ttk controls."""
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    style.configure(
        ".",
        background=BG_PRIMARY,
        foreground=FG_PRIMARY,
        font=(FONT_FAMILY, 10),
    )
    style.configure(
        "Section.TLabel",
        background=BG_SECONDARY,
        foreground=ACCENT_CYAN,
        font=(FONT_FAMILY, 10, "bold"),
    )
    style.configure(
        "Field.TLabel",
        background=BG_SECONDARY,
        foreground=FG_PRIMARY,
        font=(FONT_FAMILY, 9, "bold"),
    )
    style.configure(
        "TRadiobutton",
        background=BG_SECONDARY,
        foreground=FG_PRIMARY,
        font=(FONT_FAMILY, 9),
    )
    style.map(
        "TRadiobutton",
        background=[("active", BG_SECONDARY)],
        foreground=[("active", ACCENT_CYAN)],
    )
    style.configure(
        "TCombobox",
        fieldbackground=BG_INPUT,
        background=BG_CARD,
        foreground=FG_PRIMARY,
        arrowcolor=FG_PRIMARY,
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", BG_INPUT)],
        foreground=[("readonly", FG_PRIMARY)],
        selectbackground=[("readonly", BG_INPUT)],
        selectforeground=[("readonly", FG_PRIMARY)],
    )
    style.configure(
        "Treeview",
        background=BG_INPUT,
        fieldbackground=BG_INPUT,
        foreground=FG_PRIMARY,
        rowheight=26,
        font=(FONT_FAMILY, 9),
    )
    style.configure(
        "Treeview.Heading",
        background=BG_CARD,
        foreground=ACCENT_CYAN,
        font=(FONT_FAMILY, 9, "bold"),
        relief="flat",
    )
    style.map(
        "Treeview",
        background=[("selected", ACCENT_CYAN)],
        foreground=[("selected", "#FFFFFF")],
    )


class DateEntrySpinbox(tk.Frame):
    """Composite DateEntry + Spinbox widget displaying dates in dd/mm/aaaa format."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, bg=BG_SECONDARY)
        today = date.today()
        self.day_var = tk.StringVar(value=f"{today.day:02d}")
        self.month_var = tk.StringVar(value=f"{today.month:02d}")
        self.year_var = tk.StringVar(value=f"{today.year:04d}")
        self.formatted_date_var = tk.StringVar(value=today.strftime("%d/%m/%Y"))
        self._build_widgets()

    def _build_widgets(self) -> None:
        """Builds the formatted DateEntry box and Day, Month, and Year Spinboxes."""
        self.columnconfigure(0, weight=2)
        self.columnconfigure((1, 2, 3), weight=1)

        labels = ("Fecha (dd/mm/aaaa)", "Día", "Mes", "Año")
        for col, text in enumerate(labels):
            tk.Label(
                self,
                text=text,
                bg=BG_SECONDARY,
                fg=FG_SECONDARY,
                font=(FONT_FAMILY, 8),
            ).grid(row=0, column=col, sticky="w", padx=2 if col > 0 else 0)

        self.date_entry = tk.Entry(
            self,
            textvariable=self.formatted_date_var,
            state="readonly",
            readonlybackground=BG_INPUT,
            fg=ACCENT_CYAN,
            font=(FONT_FAMILY, 9, "bold"),
            relief="solid",
            bd=1,
            width=12,
            justify="center",
        )
        self.date_entry.grid(row=1, column=0, sticky="ew", padx=(0, 4), ipady=2)

        self.day_spinbox = ttk.Spinbox(
            self,
            from_=1,
            to=31,
            textvariable=self.day_var,
            width=4,
            format="%02.0f",
            command=self._on_arrow_click,
        )
        self.day_spinbox.grid(row=1, column=1, sticky="ew", padx=2)

        self.month_spinbox = ttk.Spinbox(
            self,
            from_=1,
            to=12,
            textvariable=self.month_var,
            width=4,
            format="%02.0f",
            command=self._on_arrow_click,
        )
        self.month_spinbox.grid(row=1, column=2, sticky="ew", padx=2)

        self.year_spinbox = ttk.Spinbox(
            self,
            from_=1950,
            to=2100,
            textvariable=self.year_var,
            width=6,
            command=self._on_arrow_click,
        )
        self.year_spinbox.grid(row=1, column=3, sticky="ew", padx=(2, 0))

        for spinbox in (self.day_spinbox, self.month_spinbox, self.year_spinbox):
            spinbox.bind("<KeyRelease>", lambda _e: self._sync_raw_fields())
            spinbox.bind("<FocusOut>", lambda _e: self._sync_raw_fields())

    def _on_arrow_click(self) -> None:
        """Adjusts day limits according to month and year when clicking Spinbox arrows."""
        try:
            year = max(1950, min(2100, int(self.year_var.get())))
            month = max(1, min(12, int(self.month_var.get())))
            max_day = calendar.monthrange(year, month)[1]
            day = max(1, min(max_day, int(self.day_var.get())))
            self.day_spinbox.configure(to=max_day)
            self.day_var.set(f"{day:02d}")
            self.month_var.set(f"{month:02d}")
            self.year_var.set(f"{year:04d}")
            self.formatted_date_var.set(f"{day:02d}/{month:02d}/{year:04d}")
        except ValueError:
            self._sync_raw_fields()

    def _sync_raw_fields(self) -> None:
        """Synchronizes the DateEntry field with manually typed Spinbox values."""
        raw_day = self.day_var.get().strip()
        raw_month = self.month_var.get().strip()
        raw_year = self.year_var.get().strip()
        day_token = raw_day.zfill(2) if (raw_day.isdigit() and len(raw_day) <= 2) else raw_day
        month_token = (
            raw_month.zfill(2) if (raw_month.isdigit() and len(raw_month) <= 2) else raw_month
        )
        self.formatted_date_var.set(f"{day_token}/{month_token}/{raw_year}")

    def get_date_string(self) -> str:
        """Returns the current date formatted as dd/mm/aaaa."""
        self._sync_raw_fields()
        return self.formatted_date_var.get().strip()

    def reset_to_today(self) -> None:
        """Resets the selector to the current system date."""
        today = date.today()
        self.day_var.set(f"{today.day:02d}")
        self.month_var.set(f"{today.month:02d}")
        self.year_var.set(f"{today.year:04d}")
        self.formatted_date_var.set(today.strftime("%d/%m/%Y"))
