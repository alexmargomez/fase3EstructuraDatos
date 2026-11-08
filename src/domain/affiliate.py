"""Entidad de dominio que representa un afiliado de la Caja Compensándote."""

from dataclasses import dataclass
import math
from typing import Tuple

from src.config.constants import (
    DESIRED_SERVICES,
    EMPLOYMENT_MODES,
    ID_TYPES,
    MAX_ALLOWED_INCOME,
    MIN_ALLOWED_INCOME,
)


@dataclass(frozen=True)
class Affiliate:
    """Modelo inmutable de datos del afiliado."""

    id_type: str
    id_number: str
    full_name: str
    current_income: float
    desired_service: str
    employment_mode: str
    affiliation_fee: float
    affiliation_date: str

    def __post_init__(self) -> None:
        """Valida invariantes básicas de dominio al instanciar el afiliado."""
        normalized_id_type = self.id_type.strip()
        normalized_id_number = self.id_number.strip()
        normalized_full_name = " ".join(self.full_name.strip().split())
        normalized_service = self.desired_service.strip()
        normalized_employment = self.employment_mode.strip()
        normalized_date = self.affiliation_date.strip()

        object.__setattr__(self, "id_type", normalized_id_type)
        object.__setattr__(self, "id_number", normalized_id_number)
        object.__setattr__(self, "full_name", normalized_full_name)
        object.__setattr__(self, "desired_service", normalized_service)
        object.__setattr__(self, "employment_mode", normalized_employment)
        object.__setattr__(self, "affiliation_date", normalized_date)

        if normalized_id_type not in ID_TYPES:
            raise ValueError(f"Tipo de identificación inválido: '{normalized_id_type}'.")
        if (
            not normalized_id_number
            or not (normalized_id_number.isascii() and normalized_id_number.isdigit())
            or int(normalized_id_number) == 0
        ):
            raise ValueError(
                "El número de identificación debe contener dígitos numéricos válidos."
            )
        if not normalized_full_name:
            raise ValueError("El nombre completo del afiliado no puede estar vacío.")
        if (
            isinstance(self.current_income, bool)
            or not math.isfinite(self.current_income)
            or self.current_income < MIN_ALLOWED_INCOME
            or self.current_income > MAX_ALLOWED_INCOME
        ):
            raise ValueError(
                "Los ingresos actuales deben estar entre $1.000.000 y $1.000.000.000."
            )
        if normalized_service not in DESIRED_SERVICES:
            raise ValueError(f"Servicio deseado inválido: '{normalized_service}'.")
        if normalized_employment not in EMPLOYMENT_MODES:
            raise ValueError(f"Modalidad de empleo inválida: '{normalized_employment}'.")
        if (
            isinstance(self.affiliation_fee, bool)
            or not math.isfinite(self.affiliation_fee)
            or self.affiliation_fee < 0.0
        ):
            raise ValueError("La tarifa de afiliación no puede ser negativa.")
        if not normalized_date:
            raise ValueError("La fecha de afiliación es obligatoria.")

    def to_tuple(self) -> Tuple[str, str, str, float, str, str, float, str]:
        """Retorna los atributos del afiliado como tupla de valores primitivos."""
        return (
            self.id_type,
            self.id_number,
            self.full_name,
            self.current_income,
            self.desired_service,
            self.employment_mode,
            self.affiliation_fee,
            self.affiliation_date,
        )


# Alias compatibles con la guía Anexo 2
AffiliateDataStructure = Affiliate
EstructuraDatosAfiliado = Affiliate
