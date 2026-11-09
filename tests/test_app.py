"""Unit tests for the Compensándote MVC application (Models, Controller, and Views)."""

import tkinter as tk
import unittest

from controllers.affiliate_controller import AffiliateController
from models.affiliate import Affiliate, EstructuraDatosAfiliado
from models.structures import AffiliateList, AffiliateQueue, AffiliateStack
from views.affiliate_view import AffiliateView
from views.login_view import LoginView


class TestCompensandoteMVC(unittest.TestCase):
    """Verifies domain structures, fee calculation, validations, and MVC views."""

    def setUp(self) -> None:
        self.controller = AffiliateController()

    def _sample_affiliate(
        self,
        id_number: str = "1010",
        full_name: str = "Carlos Andres Perez",
        current_income: float = 2_500_000.0,
        desired_service: str = "Ingreso a parque",
        employment_mode: str = "Empleado",
    ) -> Affiliate:
        return self.controller.create_affiliate(
            id_type="CC",
            id_number=id_number,
            full_name=full_name,
            current_income_text=str(current_income),
            desired_service=desired_service,
            employment_mode=employment_mode,
            affiliation_date_text="09/11/2026",
        )

    def test_password_and_entity_alias(self) -> None:
        """Checks password validation ('Caja') and EstructuraDatosAfiliado alias."""
        self.assertIs(EstructuraDatosAfiliado, Affiliate)
        self.assertTrue(self.controller.validate_password("Caja"))
        self.assertFalse(self.controller.validate_password("caja"))
        self.assertFalse(self.controller.validate_password(""))

    def test_fee_calculation_tables_2_and_3(self) -> None:
        """Checks boundary values for Table 2 (Empleado), Table 3 (Independiente), and surcharges."""
        with self.assertRaises(ValueError):
            self.controller.calculate_fee(999_999.0, "Empleado", "Subsidio de desempleo")

        employee_tiers = (
            (1_000_000.0, 45_000.0),
            (2_000_000.0, 45_000.0),
            (2_500_000.0, 60_000.0),
            (3_500_000.0, 75_000.0),
            (4_500_000.0, 90_000.0),
            (5_500_000.0, 150_000.0),
        )
        for income, expected in employee_tiers:
            self.assertEqual(
                self.controller.calculate_fee(income, "Empleado", "Subsidio de desempleo"),
                expected,
            )

        independent_tiers = (
            (1_000_000.0, 10_000.0),
            (2_000_000.0, 10_000.0),
            (2_500_000.0, 20_000.0),
            (3_500_000.0, 30_000.0),
            (4_500_000.0, 40_000.0),
            (5_500_000.0, 80_000.0),
        )
        for income, expected in independent_tiers:
            self.assertEqual(
                self.controller.calculate_fee(
                    income, "Independiente", "Subsidio de desempleo"
                ),
                expected,
            )

        # Service surcharges
        self.assertEqual(
            self.controller.calculate_fee(2_000_000.0, "Empleado", "Ingreso a parque"),
            47_500.0,
        )
        self.assertEqual(
            self.controller.calculate_fee(2_000_000.0, "Empleado", "Curso de formación"),
            52_500.0,
        )
        self.assertEqual(
            self.controller.calculate_fee(2_000_000.0, "Empleado", "Paquete de viaje"),
            55_000.0,
        )
        self.assertEqual(
            self.controller.calculate_fee(2_000_000.0, "Empleado", "Medicina preventiva"),
            245_000.0,
        )

    def test_stack_queue_and_list_operations(self) -> None:
        """Verifies LIFO Stack, FIFO Queue, Sequential List, and their reports."""
        a1 = self._sample_affiliate("101", "Ana Maria", 1_500_000.0)
        a2 = self._sample_affiliate("102", "Luis Fernando", 2_500_000.0)

        # Stack (LIFO)
        stack = AffiliateStack()
        stack.push(a1)
        stack.push(a2)
        self.assertEqual(stack.get_total_fees(), a1.affiliation_fee + a2.affiliation_fee)
        self.assertEqual(stack.pop(), a2)

        # Queue (FIFO)
        queue = AffiliateQueue()
        queue.enqueue(a1)
        queue.enqueue(a2)
        self.assertEqual(queue.get_record_count(), 2)
        self.assertEqual(queue.dequeue(), a1)

        # List (Sequential + ID search/delete)
        alist = AffiliateList()
        alist.add(a1)
        alist.add(a2)
        self.assertEqual(alist.get_average_income(), 2_000_000.0)
        self.assertEqual(alist.remove_by_id("101"), a1)
        self.assertIsNone(alist.find_by_id("101"))

    def test_views_and_report_button(self) -> None:
        """Verifies LoginView, AffiliateView reactive fee, and Reporte button behavior."""
        try:
            root = tk.Tk()
            root.withdraw()
        except tk.TclError:
            self.skipTest("X11 display not available")
            return

        try:
            login_view = LoginView(root, self.controller, on_login_success=lambda: None)
            login_view.toggle_password_mask()
            self.assertEqual(login_view.password_entry.cget("show"), "")
            login_view.destroy_view()

            view = AffiliateView(root, self.controller)
            view.current_income_var.set("2500000")
            view.employment_mode_var.set("Empleado")
            view.desired_service_var.set("Ingreso a parque")
            self.assertEqual(view.affiliation_fee_var.get(), "$62,500.00")

            view.id_type_var.set("CC")
            view.id_number_var.set("900100")
            view.full_name_var.set("Fabio Alexmar Gomez")
            view.structure_var.set("Lista")
            view.handle_register()

            self.assertEqual(len(self.controller.affiliate_list.get_all()), 1)
            self.assertEqual(view.report_var.get(), "")

            view.handle_report()
            self.assertIn("$2,500,000.00", view.report_var.get())

            view.handle_clear()
            self.assertEqual(view.report_var.get(), "")
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()
