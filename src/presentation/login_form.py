"""Ventana de inicio de sesión y diálogo modal Acerca de (RF-01)."""

import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional

from src.config.constants import (
    ABOUT_WINDOW_TITLE,
    APPLICATION_DATE,
    COLLABORATIVE_GROUP,
    COURSE_CODE,
    COURSE_NAME,
    LOGIN_WINDOW_TITLE,
    PROJECT_NAME,
    STUDENT_NAME,
    UNIVERSITY_INFO,
)
from src.presentation.theme import (
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
    apply_application_theme,
)
from src.services.data_validation_service import DataValidationService


class LoginForm:
    """Interfaz inicial de autenticación 'Login - Compensándote'."""

    def __init__(
        self,
        root: tk.Tk,
        on_login_success: Callable[[], None],
    ) -> None:
        self.root = root
        self.on_login_success = on_login_success
        self.password_var = tk.StringVar()
        self._is_password_masked = True
        self._about_dialog: Optional[tk.Toplevel] = None
        self._main_frame: Optional[tk.Frame] = None

        self._configure_window()
        self._build_menu_bar()
        self._build_ui()

    def _configure_window(self) -> None:
        """Configura título, dimensiones y centrado de la ventana de login."""
        apply_application_theme(self.root)
        self.root.title(LOGIN_WINDOW_TITLE)
        self.root.configure(bg=BG_PRIMARY)
        self.root.resizable(False, False)

        width = 480
        height = 560
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        pos_x = max(0, (screen_width - width) // 2)
        pos_y = max(0, (screen_height - height) // 2)
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def _build_menu_bar(self) -> None:
        """Crea el menú superior con la opción Acerca de (Figuras 1 y 2)."""
        menu_bar = tk.Menu(self.root)
        menu_bar.add_command(label="Acerca de", command=self.show_about_dialog)
        self.root.config(menu=menu_bar)

    def _build_ui(self) -> None:
        """Construye los controles visuales del formulario de autenticación."""
        self._main_frame = tk.Frame(self.root, bg=BG_PRIMARY)
        self._main_frame.pack(fill=tk.BOTH, expand=True)

        top_stripe = tk.Frame(self._main_frame, bg=ACCENT_CYAN, height=4)
        top_stripe.pack(fill=tk.X)

        container = tk.Frame(self._main_frame, bg=BG_PRIMARY, padx=32, pady=20)
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

        metadata_rows = (
            ("Aplicación:", PROJECT_NAME),
            ("Estudiante:", STUDENT_NAME),
            ("Curso:", f"{COURSE_NAME} · {COURSE_CODE}"),
            ("Grupo:", COLLABORATIVE_GROUP),
            ("Fecha:", APPLICATION_DATE),
        )
        for row_idx, (label_text, value_text) in enumerate(metadata_rows):
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
        self.password_entry.bind("<Return>", self._handle_enter_key)
        self.password_entry.focus_set()

        self.toggle_mask_button = tk.Button(
            password_frame,
            text="Ver",
            command=self._toggle_password_visibility,
            bg=BG_CARD,
            fg=FG_SECONDARY,
            activebackground=ACCENT_SLATE,
            activeforeground=FG_PRIMARY,
            font=(FONT_FAMILY, 8, "bold"),
            relief="flat",
            padx=8,
            cursor="hand2",
        )
        self.toggle_mask_button.pack(side=tk.RIGHT, padx=4, pady=4)

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

        self.login_button = tk.Button(
            buttons_frame,
            text="Ingresar",
            command=self.handle_login,
            bg=ACCENT_CYAN,
            fg="#FFFFFF",
            activebackground="#138496",
            activeforeground="#FFFFFF",
            font=(FONT_FAMILY, 10, "bold"),
            relief="flat",
            pady=9,
            cursor="hand2",
        )
        self.login_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.exit_button = tk.Button(
            buttons_frame,
            text="Salir",
            command=self.handle_exit,
            bg=ACCENT_RED,
            fg="#FFFFFF",
            activebackground="#B02A37",
            activeforeground="#FFFFFF",
            font=(FONT_FAMILY, 10, "bold"),
            relief="flat",
            pady=9,
            cursor="hand2",
        )
        self.exit_button.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        # Botón Acerca de requerido por el Anexo 2
        self.about_button = tk.Button(
            container,
            text="Acerca de",
            command=self.show_about_dialog,
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
        )
        self.about_button.pack(fill=tk.X, pady=(2, 10))

        tk.Label(
            container,
            text=UNIVERSITY_INFO,
            bg=BG_PRIMARY,
            fg=FG_SECONDARY,
            font=(FONT_FAMILY, 8),
        ).pack(side=tk.BOTTOM)

    def destroy_view(self) -> None:
        """Limpia el menú y destruye el contenedor de login antes de abrir el formulario principal."""
        if self._about_dialog is not None and self._about_dialog.winfo_exists():
            self._about_dialog.destroy()
            self._about_dialog = None
        self.root.config(menu="")
        if self._main_frame is not None and self._main_frame.winfo_exists():
            self._main_frame.destroy()
            self._main_frame = None

    def _toggle_password_visibility(self) -> None:
        """Alterna el enmascaramiento de la contraseña entre '*' y texto visible."""
        self._is_password_masked = not self._is_password_masked
        self.password_entry.configure(show="*" if self._is_password_masked else "")
        self.toggle_mask_button.configure(
            text="Ver" if self._is_password_masked else "Ocultar"
        )

    def _handle_enter_key(self, _event: tk.Event) -> None:  # type: ignore[type-arg]
        """Ejecuta la validación de ingreso al presionar Enter."""
        self.handle_login()

    def handle_login(self) -> None:
        """Valida la clave ingresada ('Caja') y redirige al formulario de afiliados."""
        entered_password = self.password_var.get()
        if not entered_password:
            messagebox.showerror(
                "Error de Autenticación",
                "Por favor digite la contraseña de acceso.",
                parent=self.root,
            )
            self.password_entry.focus_set()
            return

        if not DataValidationService.validate_password(entered_password):
            messagebox.showerror(
                "Acceso Denegado",
                "La contraseña ingresada es incorrecta. Verifique e intente nuevamente.",
                parent=self.root,
            )
            self.password_var.set("")
            self.password_entry.focus_set()
            return

        self.on_login_success()

    def show_about_dialog(self) -> None:
        """Muestra el cuadro de diálogo modal Acerca de con los datos del curso y estudiante."""
        if self._about_dialog is not None and self._about_dialog.winfo_exists():
            self._about_dialog.lift()
            self._about_dialog.focus_force()
            return

        self.root.update_idletasks()
        dialog = tk.Toplevel(self.root)
        self._about_dialog = dialog
        dialog.title(ABOUT_WINDOW_TITLE)
        dialog.configure(bg=BG_SECONDARY)
        dialog.resizable(False, False)
        dialog.transient(self.root)

        width = 420
        height = 290
        pos_x = self.root.winfo_rootx() + (self.root.winfo_width() - width) // 2
        pos_y = self.root.winfo_rooty() + (self.root.winfo_height() - height) // 2
        dialog.geometry(f"{width}x{height}+{max(0, pos_x)}+{max(0, pos_y)}")

        body = tk.Frame(dialog, bg=BG_SECONDARY, padx=24, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            body,
            text="Acerca de la Aplicación",
            bg=BG_SECONDARY,
            fg=ACCENT_CYAN,
            font=(FONT_FAMILY, 13, "bold"),
            anchor="w",
        ).pack(fill=tk.X, pady=(0, 12))

        details = (
            f"Curso: {COURSE_NAME} — {COURSE_CODE}",
            f"Estudiante: {STUDENT_NAME}",
            f"Grupo Colaborativo: {COLLABORATIVE_GROUP}",
            f"Programa: {UNIVERSITY_INFO}",
            f"Fecha: {APPLICATION_DATE}",
        )
        for line in details:
            tk.Label(
                body,
                text=line,
                bg=BG_SECONDARY,
                fg=FG_PRIMARY,
                font=(FONT_FAMILY, 9),
                anchor="w",
                pady=3,
            ).pack(fill=tk.X)

        def _close_dialog(_event: object = None) -> None:
            if dialog.winfo_exists():
                dialog.destroy()
            self._about_dialog = None
            if self.password_entry.winfo_exists():
                self.password_entry.focus_set()

        accept_btn = tk.Button(
            body,
            text="Aceptar",
            command=_close_dialog,
            bg=ACCENT_CYAN,
            fg="#FFFFFF",
            activebackground="#138496",
            activeforeground="#FFFFFF",
            font=(FONT_FAMILY, 9, "bold"),
            relief="flat",
            padx=18,
            pady=6,
            cursor="hand2",
        )
        accept_btn.pack(anchor="e", pady=(16, 0))

        dialog.protocol("WM_DELETE_WINDOW", _close_dialog)
        dialog.bind("<Return>", _close_dialog)
        dialog.bind("<Escape>", _close_dialog)

        dialog.update_idletasks()
        try:
            dialog.grab_set()
        except tk.TclError:
            pass
        accept_btn.focus_set()

    def handle_exit(self) -> None:
        """Finaliza la ejecución de la aplicación."""
        self.root.destroy()
