"""Punto de entrada principal de la aplicación Caja Compensándote."""

from src.presentation.app_controller import ApplicationController


def main() -> None:
    """Inicializa y ejecuta la aplicación de control de afiliados."""
    controller = ApplicationController()
    controller.start()


if __name__ == "__main__":
    main()
