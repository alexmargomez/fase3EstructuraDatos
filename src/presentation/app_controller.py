"""Controlador de aplicación que coordina el paso entre LoginForm y AffiliateForm."""

import tkinter as tk
from typing import Optional

from src.domain.data_structures import AffiliateRepository
from src.presentation.affiliate_form import AffiliateForm
from src.presentation.login_form import LoginForm


class ApplicationController:
    """Gestiona el ciclo de vida de las ventanas de la aplicación."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.repository = AffiliateRepository()
        self.login_form: Optional[LoginForm] = None
        self.affiliate_form: Optional[AffiliateForm] = None

    def start(self) -> None:
        """Inicia la ventana de autenticación y el bucle principal de Tkinter."""
        self.login_form = LoginForm(
            root=self.root,
            on_login_success=self.transition_to_main_form,
        )
        self.root.mainloop()

    def transition_to_main_form(self) -> None:
        """Cierra la vista de login y despliega el formulario principal de afiliados."""
        if self.login_form is not None:
            self.login_form.destroy_view()
            self.login_form = None
        self.affiliate_form = AffiliateForm(
            root=self.root,
            repository=self.repository,
        )
