"""Control compuesto DateEntry + Spinbox para captura de fecha en formato dd/mm/aaaa."""

import calendar
from datetime import date
import tkinter as tk
from tkinter import ttk

from src.config.constants import DATE_FORMAT, MAX_ALLOWED_YEAR, MIN_ALLOWED_YEAR
from src.presentation.theme import (
    ACCENT_CYAN,
    BG_INPUT,
    BG_SECONDARY,
    FG_SECONDARY,
    FONT_FAMILY,
)


class DateEntrySpinbox(tk.Frame):
    """Combina selectores Spinbox (Día, Mes, Año) con un campo DateEntry formateado."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, bg=BG_SECONDARY)
        today = date.today()

        self.day_var = tk.StringVar(value=f"{today.day:02d}")
        self.month_var = tk.StringVar(value=f"{today.month:02d}")
        self.year_var = tk.StringVar(value=f"{today.year:04d}")
        self.formatted_date_var = tk.StringVar(value=today.strftime(DATE_FORMAT))

        self._build_controls()
        self._update_from_raw_fields()

    @staticmethod
    def _is_valid_spinbox_digits(text: str) -> bool:
        """Permite únicamente hasta 4 dígitos numéricos en cada Spinbox."""
        if text == "":
            return True
        return text.isascii() and text.isdigit() and len(text) <= 4

    def _build_controls(self) -> None:
        """Construye la fila compacta con DateEntry y Spinboxes de Día, Mes y Año."""
        self.columnconfigure(0, weight=2)
        self.columnconfigure((1, 2, 3), weight=1)

        tk.Label(
            self,
            text="Fecha (dd/mm/aaaa)",
            bg=BG_SECONDARY,
            fg=FG_SECONDARY,
            font=(FONT_FAMILY, 8),
        ).grid(row=0, column=0, sticky="w", padx=(0, 4))
        tk.Label(
            self,
            text="Día",
            bg=BG_SECONDARY,
            fg=FG_SECONDARY,
            font=(FONT_FAMILY, 8),
        ).grid(row=0, column=1, sticky="w", padx=2)
        tk.Label(
            self,
            text="Mes",
            bg=BG_SECONDARY,
            fg=FG_SECONDARY,
            font=(FONT_FAMILY, 8),
        ).grid(row=0, column=2, sticky="w", padx=2)
        tk.Label(
            self,
            text="Año",
            bg=BG_SECONDARY,
            fg=FG_SECONDARY,
            font=(FONT_FAMILY, 8),
        ).grid(row=0, column=3, sticky="w", padx=(2, 0))

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

        vcmd = (self.register(self._is_valid_spinbox_digits), "%P")

        self.day_spinbox = ttk.Spinbox(
            self,
            from_=1,
            to=31,
            textvariable=self.day_var,
            width=4,
            format="%02.0f",
            validate="key",
            validatecommand=vcmd,
            command=self._on_spinbox_arrow,
        )
        self.day_spinbox.grid(row=1, column=1, sticky="ew", padx=2)

        self.month_spinbox = ttk.Spinbox(
            self,
            from_=1,
            to=12,
            textvariable=self.month_var,
            width=4,
            format="%02.0f",
            validate="key",
            validatecommand=vcmd,
            command=self._on_spinbox_arrow,
        )
        self.month_spinbox.grid(row=1, column=2, sticky="ew", padx=2)

        self.year_spinbox = ttk.Spinbox(
            self,
            from_=MIN_ALLOWED_YEAR,
            to=MAX_ALLOWED_YEAR,
            textvariable=self.year_var,
            width=6,
            validate="key",
            validatecommand=vcmd,
            command=self._on_spinbox_arrow,
        )
        self.year_spinbox.grid(row=1, column=3, sticky="ew", padx=(2, 0))

        for spinbox in (self.day_spinbox, self.month_spinbox, self.year_spinbox):
            spinbox.bind("<KeyRelease>", self._on_manual_entry)
            spinbox.bind("<FocusOut>", self._on_manual_entry)

    def _on_spinbox_arrow(self) -> None:
        """Ajusta los días válidos del mes al usar las flechas de los Spinbox."""
        try:
            year = max(MIN_ALLOWED_YEAR, min(MAX_ALLOWED_YEAR, int(self.year_var.get())))
            month = max(1, min(12, int(self.month_var.get())))
            max_day = calendar.monthrange(year, month)[1]
            day = max(1, min(max_day, int(self.day_var.get())))

            self.day_spinbox.configure(to=max_day)
            self.day_var.set(f"{day:02d}")
            self.month_var.set(f"{month:02d}")
            self.year_var.set(f"{year:04d}")
            self.formatted_date_var.set(f"{day:02d}/{month:02d}/{year:04d}")
        except ValueError:
            self._update_from_raw_fields()

    def _on_manual_entry(self, _event: object = None) -> None:
        """Actualiza la cadena de fecha preservando valores digitados manualmente."""
        self._update_from_raw_fields()

    def _update_from_raw_fields(self) -> None:
        """Sincroniza el campo DateEntry con los valores actuales de Día, Mes y Año."""
        raw_day = self.day_var.get().strip()
        raw_month = self.month_var.get().strip()
        raw_year = self.year_var.get().strip()

        day_token = raw_day.zfill(2) if (raw_day.isdigit() and len(raw_day) <= 2) else raw_day
        month_token = (
            raw_month.zfill(2) if (raw_month.isdigit() and len(raw_month) <= 2) else raw_month
        )
        self.formatted_date_var.set(f"{day_token}/{month_token}/{raw_year}")

    def get_date_string(self) -> str:
        """Retorna la fecha en formato dd/mm/aaaa para su validación."""
        self._update_from_raw_fields()
        return self.formatted_date_var.get().strip()

    def reset_to_today(self) -> None:
        """Restablece la fecha a la fecha actual del sistema."""
        today = date.today()
        max_day = calendar.monthrange(today.year, today.month)[1]
        self.day_spinbox.configure(to=max_day)
        self.day_var.set(f"{today.day:02d}")
        self.month_var.set(f"{today.month:02d}")
        self.year_var.set(f"{today.year:04d}")
        self.formatted_date_var.set(today.strftime(DATE_FORMAT))
