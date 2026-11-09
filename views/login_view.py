"""LoginView window ('Login - Compensándote') and 'Acerca de' modal dialog."""

import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional

from controllers.affiliate_controller import (
    APPLICATION_DATE,
    COLLABORATIVE_GROUP,
    COURSE_CODE,
    COURSE_NAME,
    PROJECT_NAME,
    STUDENT_NAME,
    UNIVERSITY_INFO,
    AffiliateController,
)
from views.theme import (
    ABOUT_WINDOW_TITLE,
    ACCENT_CYAN,
    ACCENT_RED,
    ACCENT_SLATE,
    BG_CARD,
    BG_INPUT,
    BG_PRIMARY,
    BG_SECONDARY,
    BORDER_COLOR,
    FG_PRIMARY,
    FG_SECONDARY,
    FONT_FAMILY,
    LOGIN_WINDOW_TITLE,
    apply_theme,
)


class LoginView:
    """Authentication GUI window with masked password ('Caja') and About dialog."""

    def __init__(
        self,
        root: tk.Tk,
        controller: AffiliateController,
        on_login_success: Callable[[], None],
    ) -> None:
        self.root = root
        self.controller = controller
        self.on_login_success = on_login_success
        self.password_var = tk.StringVar()
        self.is_masked = True
        self.main_frame: Optional[tk.Frame] = None

        self._configure_window()
        self._build_menu()
        self._build_widgets()

    def _configure_window(self) -> None:
        """Sets window title, dimensions, and screen centering."""
        apply_theme(self.root)
        self.root.title(LOGIN_WINDOW_TITLE)
        self.root.configure(bg=BG_PRIMARY)
        self.root.resizable(False, False)

        width, height = 480, 560
        pos_x = max(0, (self.root.winfo_screenwidth() - width) // 2)
        pos_y = max(0, (self.root.winfo_screenheight() - height) // 2)
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def _build_menu(self) -> None:
        """Creates the top menu bar with the 'Acerca de' option."""
        menu_bar = tk.Menu(self.root)
        menu_bar.add_command(label="Acerca de", command=self.show_about)
        self.root.config(menu=menu_bar)

    def _build_widgets(self) -> None:
        """Builds the authentication form widgets."""
        self.main_frame = tk.Frame(self.root, bg=BG_PRIMARY)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Frame(self.main_frame, bg=ACCENT_CYAN, height=4).pack(fill=tk.X)

        container = tk.Frame(self.main_frame, bg=BG_PRIMARY, padx=32, pady=20)
        container.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            container,
            text="Compensándote",
            bg=BG_PRIMARY,
            fg=ACCENT_CYAN,
            font=(FONT_FAMILY, 22, "bold"),
        ).pack(pady=(2, 2))

        tk.Label(
            container,
            text="Caja de Compensación Familiar — Control de Afiliados",
            bg=BG_PRIMARY,
            fg=FG_SECONDARY,
            font=(FONT_FAMILY, 9),
        ).pack(pady=(0, 16))

        info_card = tk.Frame(
            container,
            bg=BG_SECONDARY,
            highlightbackground=ACCENT_CYAN,
            highlightthickness=1,
            padx=16,
            pady=10,
        )
        info_card.pack(fill=tk.X, pady=(0, 18))
        info_card.columnconfigure(1, weight=1)

        metadata = (
            ("Aplicación:", PROJECT_NAME),
            ("Estudiante:", STUDENT_NAME),
            ("Curso:", f"{COURSE_NAME} · {COURSE_CODE}"),
            ("Grupo:", COLLABORATIVE_GROUP),
            ("Fecha:", APPLICATION_DATE),
        )
        for row_idx, (label_text, value_text) in enumerate(metadata):
            tk.Label(
                info_card,
                text=label_text,
                bg=BG_SECONDARY,
                fg=FG_SECONDARY,
                font=(FONT_FAMILY, 9),
                anchor="w",
            ).grid(row=row_idx, column=0, sticky="w", pady=2, padx=(0, 12))
            tk.Label(
                info_card,
                text=value_text,
                bg=BG_SECONDARY,
                fg=FG_PRIMARY,
                font=(FONT_FAMILY, 9, "bold"),
                anchor="w",
            ).grid(row=row_idx, column=1, sticky="w", pady=2)

        tk.Label(
            container,
            text="Contraseña de Acceso",
            bg=BG_PRIMARY,
            fg=FG_PRIMARY,
            font=(FONT_FAMILY, 10, "bold"),
            anchor="w",
        ).pack(fill=tk.X, pady=(0, 6))

        password_frame = tk.Frame(
            container,
            bg=BG_INPUT,
            highlightbackground=ACCENT_CYAN,
            highlightthickness=1,
        )
        password_frame.pack(fill=tk.X)

        self.password_entry = tk.Entry(
            password_frame,
            textvariable=self.password_var,
            show="*",
            bg=BG_INPUT,
            fg=FG_PRIMARY,
            insertbackground=FG_PRIMARY,
            font=(FONT_FAMILY, 11),
            relief="flat",
            bd=8,
        )
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.password_entry.bind("<Return>", lambda _e: self.login())
        self.password_entry.focus_set()

        self.toggle_button = tk.Button(
            password_frame,
            text="Ver",
            command=self.toggle_password_mask,
            bg=BG_CARD,
            fg=FG_SECONDARY,
            activebackground=ACCENT_SLATE,
            activeforeground=FG_PRIMARY,
            font=(FONT_FAMILY, 8, "bold"),
            relief="flat",
            padx=8,
            cursor="hand2",
        )
        self.toggle_button.pack(side=tk.RIGHT, padx=4, pady=4)

        tk.Label(
            container,
            text="Campo enmascarado con (*) · Clave requerida para acceder",
            bg=BG_PRIMARY,
            fg=FG_SECONDARY,
            font=(FONT_FAMILY, 8),
            anchor="w",
        ).pack(fill=tk.X, pady=(4, 16))

        buttons_frame = tk.Frame(container, bg=BG_PRIMARY)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        buttons_frame.columnconfigure((0, 1), weight=1)

        tk.Button(
            buttons_frame,
            text="Ingresar",
            command=self.login,
            bg=ACCENT_CYAN,
            fg="#FFFFFF",
            activebackground="#138496",
            activeforeground="#FFFFFF",
            font=(FONT_FAMILY, 10, "bold"),
            relief="flat",
            pady=9,
            cursor="hand2",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        tk.Button(
            buttons_frame,
            text="Salir",
            command=self.exit_app,
            bg=ACCENT_RED,
            fg="#FFFFFF",
            activebackground="#B02A37",
            activeforeground="#FFFFFF",
            font=(FONT_FAMILY, 10, "bold"),
            relief="flat",
            pady=9,
            cursor="hand2",
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

        tk.Button(
            container,
            text="Acerca de",
            command=self.show_about,
            bg=BG_SECONDARY,
            fg=ACCENT_CYAN,
            activebackground=BG_CARD,
            activeforeground=FG_PRIMARY,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            font=(FONT_FAMILY, 9, "bold"),
            relief="flat",
            pady=7,
            cursor="hand2",
        ).pack(fill=tk.X, pady=(2, 10))

        tk.Label(
            container,
            text=UNIVERSITY_INFO,
            bg=BG_PRIMARY,
            fg=FG_SECONDARY,
            font=(FONT_FAMILY, 8),
        ).pack(side=tk.BOTTOM)

    def toggle_password_mask(self) -> None:
        """Toggles password field masking between '*' and plain text."""
        self.is_masked = not self.is_masked
        self.password_entry.configure(show="*" if self.is_masked else "")
        self.toggle_button.configure(text="Ver" if self.is_masked else "Ocultar")

    def show_about(self) -> None:
        """Shows a dialog with course name, student full name, and collaborative group."""
        messagebox.showinfo(
            ABOUT_WINDOW_TITLE,
            f"Curso: {COURSE_NAME} — {COURSE_CODE}\n"
            f"Estudiante: {STUDENT_NAME}\n"
            f"Grupo Colaborativo: {COLLABORATIVE_GROUP}\n"
            f"Programa: {UNIVERSITY_INFO}\n"
            f"Fecha: {APPLICATION_DATE}",
            parent=self.root,
        )

    def login(self) -> None:
        """Validates the entered password and transitions to the main window."""
        entered = self.password_var.get()
        if not entered:
            messagebox.showerror(
                "Error de Autenticación",
                "Por favor digite la contraseña de acceso.",
                parent=self.root,
            )
            self.password_entry.focus_set()
            return

        if not self.controller.validate_password(entered):
            messagebox.showerror(
                "Acceso Denegado",
                "La contraseña ingresada es incorrecta. Verifique e intente nuevamente.",
                parent=self.root,
            )
            self.password_var.set("")
            self.password_entry.focus_set()
            return

        self.destroy_view()
        self.on_login_success()

    def destroy_view(self) -> None:
        """Removes the Login menu and frame before displaying the main form."""
        self.root.config(menu="")
        if self.main_frame is not None and self.main_frame.winfo_exists():
            self.main_frame.destroy()
            self.main_frame = None

    def exit_app(self) -> None:
        """Terminates application execution."""
        self.root.destroy()
