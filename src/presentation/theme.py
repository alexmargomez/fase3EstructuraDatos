"""Paleta de colores y configuración de estilos visuales para Tkinter/ttk."""

import tkinter as tk
from tkinter import ttk
from typing import Final

# Paleta visual de la aplicación Compensándote
BG_PRIMARY: Final[str] = "#0F1E2E"
BG_SECONDARY: Final[str] = "#162A40"
BG_CARD: Final[str] = "#1C3550"
BG_INPUT: Final[str] = "#112233"
FG_PRIMARY: Final[str] = "#F0F6FC"
FG_SECONDARY: Final[str] = "#9FB3C8"
ACCENT_CYAN: Final[str] = "#17A2B8"
ACCENT_CYAN_HOVER: Final[str] = "#138496"
ACCENT_GREEN: Final[str] = "#198754"
ACCENT_RED: Final[str] = "#DC3545"
ACCENT_AMBER: Final[str] = "#E08E0B"
ACCENT_SLATE: Final[str] = "#3B536E"
BORDER_COLOR: Final[str] = "#284B6E"

FONT_FAMILY: Final[str] = "DejaVu Sans"


def apply_application_theme(root: tk.Misc) -> ttk.Style:
    """Configura y aplica el tema visual ttk en la ventana raíz."""
    style = ttk.Style(root)
    available_themes = style.theme_names()
    if "clam" in available_themes:
        style.theme_use("clam")

    style.configure(
        ".",
        background=BG_PRIMARY,
        foreground=FG_PRIMARY,
        font=(FONT_FAMILY, 10),
    )
    style.configure(
        "Card.TFrame",
        background=BG_SECONDARY,
        relief="flat",
    )
    style.configure(
        "Title.TLabel",
        background=BG_PRIMARY,
        foreground=ACCENT_CYAN,
        font=(FONT_FAMILY, 16, "bold"),
    )
    style.configure(
        "Subtitle.TLabel",
        background=BG_PRIMARY,
        foreground=FG_SECONDARY,
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
        "Muted.TLabel",
        background=BG_SECONDARY,
        foreground=FG_SECONDARY,
        font=(FONT_FAMILY, 8),
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
    return style
