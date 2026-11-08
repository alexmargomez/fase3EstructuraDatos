"""Servicio de generación de reportes estadísticos por estructura de datos (RF-05)."""

from decimal import Decimal, ROUND_HALF_UP

from src.config.constants import STRUCTURE_LIST, STRUCTURE_QUEUE, STRUCTURE_STACK
from src.domain.data_structures import AffiliateRepository

_CENT_PRECISION = Decimal("0.01")


class ReportService:
    """Calcula los reportes estadísticos para Pila, Cola y Lista."""

    @staticmethod
    def calculate_stack_total_fees(repository: AffiliateRepository) -> float:
        """Calcula la suma total de las tarifas de afiliación en la Pila."""
        total_dec = sum(
            (Decimal(str(item.affiliation_fee)) for item in repository.stack),
            Decimal("0.00"),
        )
        return float(total_dec.quantize(_CENT_PRECISION, rounding=ROUND_HALF_UP))

    @staticmethod
    def calculate_queue_record_count(repository: AffiliateRepository) -> int:
        """Retorna la cantidad total de registros actuales en la Cola."""
        return len(repository.queue)

    @staticmethod
    def calculate_list_average_income(repository: AffiliateRepository) -> float:
        """Calcula el promedio de ingresos actuales de los afiliados en la Lista."""
        count = len(repository.affiliate_list)
        if count == 0:
            return 0.0
        total_income_dec = sum(
            (Decimal(str(item.current_income)) for item in repository.affiliate_list),
            Decimal("0.00"),
        )
        avg_dec = (total_income_dec / Decimal(count)).quantize(
            _CENT_PRECISION,
            rounding=ROUND_HALF_UP,
        )
        return float(avg_dec)

    @classmethod
    def generate_report_text(
        cls,
        structure_type: str,
        repository: AffiliateRepository,
    ) -> str:
        """Genera el texto formateado del reporte según la estructura seleccionada."""
        if structure_type == STRUCTURE_STACK:
            total_fees = cls.calculate_stack_total_fees(repository)
            return f"Suma de tarifas de afiliación (Pila): ${total_fees:,.2f}"

        if structure_type == STRUCTURE_QUEUE:
            count = cls.calculate_queue_record_count(repository)
            suffix = "registro" if count == 1 else "registros"
            return f"Cantidad de registros en la Cola: {count} {suffix}"

        if structure_type == STRUCTURE_LIST:
            avg_income = cls.calculate_list_average_income(repository)
            return f"Promedio de ingresos actuales (Lista): ${avg_income:,.2f}"

        raise ValueError(f"Estructura de datos no reconocida: '{structure_type}'.")
