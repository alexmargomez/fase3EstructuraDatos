"""Main entry point for the Compensándote MVC application (Fase3FabioGomez)."""

import tkinter as tk

from controllers.affiliate_controller import AffiliateController
from views.affiliate_view import AffiliateView
from views.login_view import LoginView


def main() -> None:
    """Initializes the MVC components and starts the Tkinter event loop."""
    root = tk.Tk()
    controller = AffiliateController()

    def open_affiliate_view() -> None:
        AffiliateView(root=root, controller=controller)

    LoginView(
        root=root,
        controller=controller,
        on_login_success=open_affiliate_view,
    )
    root.mainloop()


if __name__ == "__main__":
    main()
