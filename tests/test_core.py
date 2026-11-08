"""Pruebas unitarias, de valores frontera (BVA), validaciones y arquitectura de Compensándote."""

import ast
from pathlib import Path
import tkinter as tk
import unittest

from src.config.constants import (
    EMPLOYMENT_EMPLOYEE,
    EMPLOYMENT_INDEPENDENT,
    SERVICE_PARK_ENTRY,
    SERVICE_PREVENTIVE_MEDICINE,
    SERVICE_TRAINING_COURSE,
    SERVICE_TRAVEL_PACKAGE,
    SERVICE_UNEMPLOYMENT_SUBSIDY,
    STRUCTURE_LIST,
    STRUCTURE_QUEUE,
    STRUCTURE_STACK,
)
from src.domain import (
    Affiliate,
    AffiliateDataStructure,
    AffiliateList,
    AffiliateQueue,
    AffiliateRepository,
    AffiliateStack,
    EstructuraDatosAfiliado,
    List,
    Queue,
    Stack,
)
from src.presentation.affiliate_form import AffiliateForm
from src.presentation.formatters import format_affiliate_treeview_row, format_currency
from src.presentation.login_form import LoginForm
from src.presentation.widgets.date_entry_spinbox import DateEntrySpinbox
from src.services.data_validation_service import DataValidationService
from src.services.fee_calculator_service import FeeCalculatorService
from src.services.report_service import ReportService


class TestCompensandoteCore(unittest.TestCase):
    """Suite de pruebas para tarifas, validaciones, estructuras lineales e interfaz."""

    def _create_sample_affiliate(
        self,
        id_number: str = "10102020",
        full_name: str = "Carlos Andres Perez",
        current_income: float = 2_500_000.0,
        desired_service: str = SERVICE_PARK_ENTRY,
        employment_mode: str = EMPLOYMENT_EMPLOYEE,
    ) -> Affiliate:
        fee = FeeCalculatorService.calculate_fee(
            current_income=current_income,
            employment_mode=employment_mode,
            desired_service=desired_service,
        )
        return Affiliate(
            id_type="CC",
            id_number=id_number,
            full_name=full_name,
            current_income=current_income,
            desired_service=desired_service,
            employment_mode=employment_mode,
            affiliation_fee=fee,
            affiliation_date="08/11/2026",
        )

    def test_password_validation(self) -> None:
        """Verifica la validación de la clave estática 'Caja'."""
        self.assertTrue(DataValidationService.validate_password("Caja"))
        self.assertFalse(DataValidationService.validate_password("caja"))
        self.assertFalse(DataValidationService.validate_password("Caja "))
        self.assertFalse(DataValidationService.validate_password(""))

    def test_employee_fee_boundary_values(self) -> None:
        """Verifica los valores límite exactos de la Tabla 2 (Empleado)."""
        with self.assertRaises(ValueError):
            FeeCalculatorService.calculate_base_fee(999_999.99, EMPLOYMENT_EMPLOYEE)

        boundary_cases = (
            (1_000_000.00, 45_000.0),
            (1_500_000.00, 45_000.0),
            (2_000_000.00, 45_000.0),
            (2_000_000.01, 60_000.0),
            (3_000_000.00, 60_000.0),
            (3_000_000.01, 75_000.0),
            (4_000_000.00, 75_000.0),
            (4_000_000.01, 90_000.0),
            (5_000_000.00, 90_000.0),
            (5_000_000.01, 150_000.0),
            (10_000_000.00, 150_000.0),
        )
        for income, expected_fee in boundary_cases:
            with self.subTest(income=income):
                self.assertEqual(
                    FeeCalculatorService.calculate_base_fee(income, EMPLOYMENT_EMPLOYEE),
                    expected_fee,
                )

    def test_independent_fee_boundary_values(self) -> None:
        """Verifica los valores límite exactos de la Tabla 3 (Independiente)."""
        with self.assertRaises(ValueError):
            FeeCalculatorService.calculate_base_fee(999_999.99, EMPLOYMENT_INDEPENDENT)

        boundary_cases = (
            (1_000_000.00, 10_000.0),
            (1_500_000.00, 10_000.0),
            (2_000_000.00, 10_000.0),
            (2_000_000.01, 20_000.0),
            (3_000_000.00, 20_000.0),
            (3_000_000.01, 30_000.0),
            (4_000_000.00, 30_000.0),
            (4_000_000.01, 40_000.0),
            (5_000_000.00, 40_000.0),
            (5_000_000.01, 80_000.0),
            (10_000_000.00, 80_000.0),
        )
        for income, expected_fee in boundary_cases:
            with self.subTest(income=income):
                self.assertEqual(
                    FeeCalculatorService.calculate_base_fee(income, EMPLOYMENT_INDEPENDENT),
                    expected_fee,
                )

    def test_service_surcharges_and_decimal_precision(self) -> None:
        """Verifica los recargos por servicio deseado y la precisión decimal."""
        income = 2_000_000.0
        self.assertEqual(
            FeeCalculatorService.calculate_fee(
                income, EMPLOYMENT_EMPLOYEE, SERVICE_UNEMPLOYMENT_SUBSIDY
            ),
            45_000.0,
        )
        self.assertEqual(
            FeeCalculatorService.calculate_fee(
                income, EMPLOYMENT_EMPLOYEE, SERVICE_PARK_ENTRY
            ),
            47_500.0,
        )
        self.assertEqual(
            FeeCalculatorService.calculate_fee(
                income, EMPLOYMENT_EMPLOYEE, SERVICE_TRAINING_COURSE
            ),
            52_500.0,
        )
        self.assertEqual(
            FeeCalculatorService.calculate_fee(
                income, EMPLOYMENT_EMPLOYEE, SERVICE_TRAVEL_PACKAGE
            ),
            55_000.0,
        )
        self.assertEqual(
            FeeCalculatorService.calculate_fee(
                income, EMPLOYMENT_EMPLOYEE, SERVICE_PREVENTIVE_MEDICINE
            ),
            245_000.0,
        )
        self.assertEqual(
            FeeCalculatorService.calculate_service_surcharge(
                1_234_567.85, SERVICE_PREVENTIVE_MEDICINE
            ),
            123_456.79,
        )

    def test_validation_service_comprehensive_chaos(self) -> None:
        """Valida el rechazo de entradas malformadas o fuera de rango en DataValidationService."""
        self.assertTrue(DataValidationService.is_valid_realtime_digits(""))
        self.assertTrue(DataValidationService.is_valid_realtime_digits("123456"))
        self.assertFalse(DataValidationService.is_valid_realtime_digits("123²"))
        self.assertFalse(DataValidationService.is_valid_realtime_digits("١٢٣٤"))
        self.assertFalse(DataValidationService.is_valid_realtime_digits("1" * 16))

        self.assertTrue(DataValidationService.is_valid_realtime_alphabetic("María José"))
        self.assertFalse(DataValidationService.is_valid_realtime_alphabetic("Juan\nPerez"))
        self.assertFalse(DataValidationService.is_valid_realtime_alphabetic("Juan123"))

        self.assertTrue(DataValidationService.is_valid_realtime_decimal("1500000.50"))
        self.assertFalse(DataValidationService.is_valid_realtime_decimal(".50"))
        self.assertFalse(DataValidationService.is_valid_realtime_decimal("1500000.555"))

        self.assertEqual(DataValidationService.validate_id_number(" 102030 "), "102030")
        for invalid_id in ("", "   ", "0", "00000", "ABC123", "123²", "١٢٣", "1" * 16):
            with self.subTest(invalid_id=invalid_id):
                with self.assertRaises(ValueError):
                    DataValidationService.validate_id_number(invalid_id)

        self.assertEqual(
            DataValidationService.validate_full_name("  María   José  Ñañez "),
            "María José Ñañez",
        )
        for invalid_name in ("", "A", "Juan\nPerez", "Juan\tPerez", "Carlos 2", "A" * 85):
            with self.subTest(invalid_name=invalid_name):
                with self.assertRaises(ValueError):
                    DataValidationService.validate_full_name(invalid_name)

        self.assertEqual(
            DataValidationService.validate_current_income("1500000.50"),
            1_500_000.50,
        )
        for invalid_income in (
            "",
            "999999.99",
            "-1500000",
            "1e7",
            "inf",
            "nan",
            "2000000.123",
            "1.500.000",
            "2000000000",
        ):
            with self.subTest(invalid_income=invalid_income):
                with self.assertRaises(ValueError):
                    DataValidationService.validate_current_income(invalid_income)

        self.assertEqual(
            DataValidationService.validate_affiliation_date("29/02/2024"),
            "29/02/2024",
        )
        for invalid_date in (
            "",
            "29/02/2026",
            "31/02/2026",
            "31/04/2026",
            "8/11/2026",
            "01/01/1949",
            "01/01/2101",
            "99/99/2026",
        ):
            with self.subTest(invalid_date=invalid_date):
                with self.assertRaises(ValueError):
                    DataValidationService.validate_affiliation_date(invalid_date)

    def test_affiliate_entity_invariants_and_decoupling(self) -> None:
        """Verifica las invariantes del modelo Affiliate y su desacoplamiento de Tkinter."""
        affiliate = self._create_sample_affiliate("  5050  ", "  Ana   Lucia ")
        self.assertEqual(affiliate.id_number, "5050")
        self.assertEqual(affiliate.full_name, "Ana Lucia")
        self.assertIs(AffiliateDataStructure, Affiliate)
        self.assertIs(EstructuraDatosAfiliado, Affiliate)
        self.assertEqual(len(affiliate.to_tuple()), 8)

        formatted_row = format_affiliate_treeview_row(affiliate)
        self.assertEqual(formatted_row[3], format_currency(affiliate.current_income))

        with self.assertRaises(ValueError):
            Affiliate(
                id_type="INVALID",
                id_number="101",
                full_name="Test Name",
                current_income=1_500_000.0,
                desired_service=SERVICE_PARK_ENTRY,
                employment_mode=EMPLOYMENT_EMPLOYEE,
                affiliation_fee=47_500.0,
                affiliation_date="08/11/2026",
            )

        with self.assertRaises(ValueError):
            Affiliate(
                id_type="CC",
                id_number="000",
                full_name="Test Name",
                current_income=1_500_000.0,
                desired_service=SERVICE_PARK_ENTRY,
                employment_mode=EMPLOYMENT_EMPLOYEE,
                affiliation_fee=47_500.0,
                affiliation_date="08/11/2026",
            )

        domain_dir = Path(__file__).resolve().parent.parent / "src" / "domain"
        for py_file in domain_dir.glob("*.py"):
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.assertNotIn("tkinter", alias.name)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    self.assertNotIn("tkinter", node.module)

    def test_stack_queue_list_edge_cases_and_repository_facade(self) -> None:
        """Prueba inserción, eliminación y reportes en Pila, Cola y Lista."""
        self.assertIs(AffiliateStack, Stack)
        self.assertIs(AffiliateQueue, Queue)
        self.assertIs(AffiliateList, List)

        repo = AffiliateRepository()
        a1 = self._create_sample_affiliate("101", "Ana Maria", 1_500_000.0)
        a2 = self._create_sample_affiliate("102", "Luis Fernando", 2_500_000.0)

        with self.assertRaises(IndexError):
            repo.remove_affiliate(STRUCTURE_STACK)
        with self.assertRaises(IndexError):
            repo.remove_affiliate(STRUCTURE_QUEUE)
        with self.assertRaises(IndexError):
            repo.remove_affiliate(STRUCTURE_LIST, target_id="101")

        self.assertEqual(ReportService.calculate_stack_total_fees(repo), 0.0)
        self.assertEqual(ReportService.calculate_queue_record_count(repo), 0)
        self.assertEqual(ReportService.calculate_list_average_income(repo), 0.0)

        repo.add_affiliate(STRUCTURE_STACK, a1)
        repo.add_affiliate(STRUCTURE_STACK, a2)
        with self.assertRaises(ValueError):
            repo.add_affiliate(STRUCTURE_STACK, a1)

        self.assertEqual(repo.peek_target_for_deletion(STRUCTURE_STACK), a2)
        self.assertEqual(
            ReportService.calculate_stack_total_fees(repo),
            a1.affiliation_fee + a2.affiliation_fee,
        )
        self.assertEqual(repo.remove_affiliate(STRUCTURE_STACK), a2)
        self.assertEqual(len(repo.stack), 1)

        repo.add_affiliate(STRUCTURE_QUEUE, a1)
        self.assertIn("1 registro", ReportService.generate_report_text(STRUCTURE_QUEUE, repo))
        repo.add_affiliate(STRUCTURE_QUEUE, a2)
        self.assertIn("2 registros", ReportService.generate_report_text(STRUCTURE_QUEUE, repo))
        with self.assertRaises(ValueError):
            repo.add_affiliate(STRUCTURE_QUEUE, a2)

        self.assertEqual(repo.peek_target_for_deletion(STRUCTURE_QUEUE), a1)
        self.assertEqual(repo.remove_affiliate(STRUCTURE_QUEUE), a1)

        repo.add_affiliate(STRUCTURE_LIST, a1)
        repo.add_affiliate(STRUCTURE_LIST, a2)
        with self.assertRaises(ValueError):
            repo.add_affiliate(STRUCTURE_LIST, a1)

        self.assertEqual(ReportService.calculate_list_average_income(repo), 2_000_000.0)
        self.assertIsNone(repo.peek_target_for_deletion(STRUCTURE_LIST, target_id="999"))
        with self.assertRaises(LookupError):
            repo.remove_affiliate(STRUCTURE_LIST, target_id="999")

        self.assertEqual(repo.remove_affiliate(STRUCTURE_LIST, target_id="101"), a1)
        self.assertFalse(repo.affiliate_list.contains_id("101"))

    def test_date_entry_spinbox_does_not_mask_invalid_manual_dates(self) -> None:
        """Verifica que DateEntrySpinbox no enmascare fechas manuales inválidas."""
        try:
            root = tk.Tk()
            root.withdraw()
        except tk.TclError:
            self.skipTest("Servidor gráfico X11 no disponible")
            return

        try:
            widget = DateEntrySpinbox(root)
            widget.day_var.set("31")
            widget.month_var.set("02")
            widget.year_var.set("2026")
            raw_date = widget.get_date_string()
            self.assertEqual(raw_date, "31/02/2026")
            with self.assertRaises(ValueError):
                DataValidationService.validate_affiliation_date(raw_date)
        finally:
            root.destroy()

    def test_ui_forms_reactive_state_and_list_selection(self) -> None:
        """Verifica reactividad de tarifas, reportes y vistas en LoginForm y AffiliateForm."""
        try:
            root = tk.Tk()
            root.withdraw()
        except tk.TclError:
            self.skipTest("Servidor gráfico X11 no disponible")
            return

        try:
            login_view = LoginForm(root=root, on_login_success=lambda: None)
            login_view._toggle_password_visibility()
            self.assertEqual(login_view.password_entry.cget("show"), "")
            login_view._toggle_password_visibility()
            self.assertEqual(login_view.password_entry.cget("show"), "*")
            login_view.destroy_view()

            form = AffiliateForm(root=root)
            form.current_income_var.set("2500000")
            form.employment_mode_var.set(EMPLOYMENT_EMPLOYEE)
            form.desired_service_var.set(SERVICE_PARK_ENTRY)
            self.assertEqual(form.affiliation_fee_var.get(), "$62,500.00")

            form.id_type_var.set("CC")
            form.id_number_var.set("900100")
            form.full_name_var.set("Fabio Alexmar Gomez")
            form.structure_type_var.set(STRUCTURE_LIST)
            form.handle_register()

            self.assertEqual(len(form.repository.affiliate_list), 1)
            self.assertEqual(form.id_number_var.get(), "")
            self.assertIn("$2,500,000.00", form.report_var.get())

            form.treeview.selection_set("900100")
            self.assertEqual(form._resolve_target_id_for_list_deletion(), "900100")
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()
