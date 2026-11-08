"""Servicio de cálculo automático de tarifas de afiliación (RF-03)."""

from decimal import Decimal, ROUND_HALF_UP
import math

from src.config.constants import (
    EMPLOYMENT_EMPLOYEE,
    EMPLOYMENT_INDEPENDENT,
    INCOME_TIER_1_MAX,
    INCOME_TIER_2_MAX,
    INCOME_TIER_3_MAX,
    INCOME_TIER_4_MAX,
    MAX_ALLOWED_INCOME,
    MIN_ALLOWED_INCOME,
    SERVICE_PARK_ENTRY,
    SERVICE_PREVENTIVE_MEDICINE,
    SERVICE_TRAINING_COURSE,
    SERVICE_TRAVEL_PACKAGE,
    SERVICE_UNEMPLOYMENT_SUBSIDY,
)

_CENT_PRECISION = Decimal("0.01")
_TEN_PERCENT = Decimal("0.10")


class FeeCalculatorService:
    """Calcula la tarifa de afiliación según ingresos, modalidad y servicio."""

    @staticmethod
    def _to_decimal(amount: float) -> Decimal:
        """Convierte un monto numérico a Decimal redondeado a dos decimales."""
        if (
            not isinstance(amount, (int, float))
            or isinstance(amount, bool)
            or not math.isfinite(amount)
        ):
            raise ValueError("El monto de ingresos debe ser un número finito válido.")
        return Decimal(str(amount)).quantize(_CENT_PRECISION, rounding=ROUND_HALF_UP)

    @classmethod
    def calculate_base_fee(cls, current_income: float, employment_mode: str) -> float:
        """Calcula la tarifa base según las Tablas 2 (Empleado) y 3 (Independiente)."""
        income_dec = cls._to_decimal(current_income)
        min_dec = Decimal(str(MIN_ALLOWED_INCOME))
        max_dec = Decimal(str(MAX_ALLOWED_INCOME))

        if income_dec < min_dec:
            raise ValueError(
                "Los ingresos actuales deben ser de al menos $1.000.000 para calcular la tarifa de afiliación."
            )
        if income_dec > max_dec:
            raise ValueError(
                "Los ingresos actuales superan el límite máximo permitido ($1.000.000.000)."
            )

        tier_1 = Decimal(str(INCOME_TIER_1_MAX))
        tier_2 = Decimal(str(INCOME_TIER_2_MAX))
        tier_3 = Decimal(str(INCOME_TIER_3_MAX))
        tier_4 = Decimal(str(INCOME_TIER_4_MAX))

        if employment_mode == EMPLOYMENT_EMPLOYEE:
            if income_dec <= tier_1:
                return 45_000.0
            if income_dec <= tier_2:
                return 60_000.0
            if income_dec <= tier_3:
                return 75_000.0
            if income_dec <= tier_4:
                return 90_000.0
            return 150_000.0

        if employment_mode == EMPLOYMENT_INDEPENDENT:
            if income_dec <= tier_1:
                return 10_000.0
            if income_dec <= tier_2:
                return 20_000.0
            if income_dec <= tier_3:
                return 30_000.0
            if income_dec <= tier_4:
                return 40_000.0
            return 80_000.0

        raise ValueError(f"Modalidad de empleo no válida: '{employment_mode}'.")

    @classmethod
    def calculate_service_surcharge(cls, current_income: float, desired_service: str) -> float:
        """Calcula el recargo adicional según el servicio deseado."""
        income_dec = cls._to_decimal(current_income)
        if income_dec < Decimal(str(MIN_ALLOWED_INCOME)):
            raise ValueError(
                "Los ingresos actuales deben ser de al menos $1.000.000 para calcular el recargo."
            )
        if income_dec > Decimal(str(MAX_ALLOWED_INCOME)):
            raise ValueError(
                "Los ingresos actuales superan el límite máximo permitido ($1.000.000.000)."
            )

        if desired_service == SERVICE_UNEMPLOYMENT_SUBSIDY:
            return 0.0
        if desired_service == SERVICE_PARK_ENTRY:
            return 2_500.0
        if desired_service == SERVICE_TRAINING_COURSE:
            return 7_500.0
        if desired_service == SERVICE_TRAVEL_PACKAGE:
            return 10_000.0
        if desired_service == SERVICE_PREVENTIVE_MEDICINE:
            surcharge_dec = (income_dec * _TEN_PERCENT).quantize(
                _CENT_PRECISION,
                rounding=ROUND_HALF_UP,
            )
            return float(surcharge_dec)

        raise ValueError(f"Servicio deseado no válido: '{desired_service}'.")

    @classmethod
    def calculate_fee(
        cls,
        current_income: float,
        employment_mode: str,
        desired_service: str,
    ) -> float:
        """Calcula la tarifa total sumando tarifa base y recargo por servicio."""
        base_fee_dec = Decimal(str(cls.calculate_base_fee(current_income, employment_mode)))
        surcharge_dec = Decimal(
            str(cls.calculate_service_surcharge(current_income, desired_service))
        )
        total_dec = (base_fee_dec + surcharge_dec).quantize(
            _CENT_PRECISION,
            rounding=ROUND_HALF_UP,
        )
        return float(total_dec)
