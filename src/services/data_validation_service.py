"""Servicio de validación de datos de entrada y reglas de negocio (RF-01, RF-02, RNF-05)."""

from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hmac
import re
from typing import Optional, Pattern

from src.config.constants import (
    DATA_STRUCTURES,
    DATE_FORMAT,
    DESIRED_SERVICES,
    EMPLOYMENT_MODES,
    ID_TYPES,
    MAX_ALLOWED_INCOME,
    MAX_ALLOWED_YEAR,
    MAX_ID_LENGTH,
    MAX_NAME_LENGTH,
    MIN_ALLOWED_INCOME,
    MIN_ALLOWED_YEAR,
    MIN_ID_LENGTH,
    MIN_NAME_LENGTH,
    STATIC_ACCESS_PASSWORD,
)
from src.domain.affiliate import Affiliate
from src.services.fee_calculator_service import FeeCalculatorService


class DataValidationService:
    """Valida credenciales de acceso y campos del formulario de afiliados."""

    _NUMERIC_ID_PATTERN: Pattern[str] = re.compile(r"^[0-9]+$", re.ASCII)
    _ALPHABETIC_NAME_PATTERN: Pattern[str] = re.compile(
        r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü]+(?: [A-Za-zÁÉÍÓÚáéíóúÑñÜü]+)*$"
    )
    _REALTIME_ALPHA_PATTERN: Pattern[str] = re.compile(
        r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]*$"
    )
    _REALTIME_DECIMAL_PATTERN: Pattern[str] = re.compile(
        r"^(?:[0-9]+(?:\.[0-9]{0,2})?)?$",
        re.ASCII,
    )
    _STRICT_DECIMAL_PATTERN: Pattern[str] = re.compile(
        r"^[0-9]+(?:\.[0-9]{1,2})?$",
        re.ASCII,
    )
    _STRICT_DATE_PATTERN: Pattern[str] = re.compile(
        r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$",
        re.ASCII,
    )

    @staticmethod
    def validate_password(password: str) -> bool:
        """Verifica si la contraseña ingresada coincide con la clave estática 'Caja'."""
        if not isinstance(password, str):
            return False
        return hmac.compare_digest(
            password.encode("utf-8"),
            STATIC_ACCESS_PASSWORD.encode("utf-8"),
        )

    @classmethod
    def is_valid_realtime_digits(cls, text: str) -> bool:
        """Filtro de teclado para permitir únicamente dígitos numéricos ASCII."""
        if text == "":
            return True
        return (
            text.isascii()
            and text.isdigit()
            and len(text) <= MAX_ID_LENGTH
        )

    @classmethod
    def is_valid_realtime_alphabetic(cls, text: str) -> bool:
        """Filtro de teclado para permitir únicamente letras y espacios."""
        if len(text) > MAX_NAME_LENGTH:
            return False
        return bool(cls._REALTIME_ALPHA_PATTERN.match(text))

    @classmethod
    def is_valid_realtime_decimal(cls, text: str) -> bool:
        """Filtro de teclado para permitir números enteros o decimales positivos."""
        if len(text) > 15:
            return False
        return bool(cls._REALTIME_DECIMAL_PATTERN.match(text))

    @classmethod
    def try_parse_valid_income(cls, income_text: str) -> Optional[float]:
        """Parsea el ingreso sin lanzar excepciones para el cálculo reactivo en la GUI."""
        cleaned = income_text.strip()
        if not cleaned or not cls._STRICT_DECIMAL_PATTERN.match(cleaned):
            return None
        try:
            income_dec = Decimal(cleaned).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        except InvalidOperation:
            return None
        min_dec = Decimal(str(MIN_ALLOWED_INCOME))
        max_dec = Decimal(str(MAX_ALLOWED_INCOME))
        if income_dec < min_dec or income_dec > max_dec:
            return None
        return float(income_dec)

    @staticmethod
    def validate_id_type(id_type: str) -> str:
        """Valida el tipo de identificación seleccionado."""
        cleaned = id_type.strip()
        if cleaned not in ID_TYPES:
            raise ValueError(
                f"Debe seleccionar un Tipo de Identificación válido ({', '.join(ID_TYPES)})."
            )
        return cleaned

    @classmethod
    def validate_id_number(cls, id_number: str) -> str:
        """Valida que el número de identificación contenga solo dígitos y no sea cero."""
        cleaned = id_number.strip()
        if not cleaned:
            raise ValueError("El campo 'Número de Identificación' es obligatorio.")
        if not cls._NUMERIC_ID_PATTERN.match(cleaned):
            raise ValueError(
                "El 'Número de Identificación' solo debe contener dígitos numéricos (0-9)."
            )
        if len(cleaned) < MIN_ID_LENGTH or len(cleaned) > MAX_ID_LENGTH:
            raise ValueError(
                f"El 'Número de Identificación' debe tener entre {MIN_ID_LENGTH} y {MAX_ID_LENGTH} dígitos."
            )
        if int(cleaned) == 0:
            raise ValueError(
                "El 'Número de Identificación' no puede estar compuesto únicamente por ceros."
            )
        return cleaned

    @classmethod
    def validate_full_name(cls, full_name: str) -> str:
        """Valida que el nombre completo solo contenga caracteres alfabéticos y espacios."""
        raw = full_name.strip()
        if not raw:
            raise ValueError("El campo 'Nombre Completo' es obligatorio.")
        if any(ch in raw for ch in ("\n", "\r", "\t", "\v", "\f")):
            raise ValueError(
                "El 'Nombre Completo' no puede contener saltos de línea ni tabulaciones."
            )
        cleaned = " ".join(raw.split())
        if len(cleaned) < MIN_NAME_LENGTH or len(cleaned) > MAX_NAME_LENGTH:
            raise ValueError(
                f"El 'Nombre Completo' debe tener entre {MIN_NAME_LENGTH} y {MAX_NAME_LENGTH} caracteres."
            )
        if not cls._ALPHABETIC_NAME_PATTERN.match(cleaned):
            raise ValueError(
                "El 'Nombre Completo' solo debe contener letras y espacios."
            )
        return cleaned

    @classmethod
    def validate_current_income(cls, income_text: str) -> float:
        """Valida que los ingresos actuales sean numéricos y mayores o iguales a $1.000.000."""
        cleaned = income_text.strip()
        if not cleaned:
            raise ValueError("El campo 'Ingresos Actuales' es obligatorio.")
        if not cls._STRICT_DECIMAL_PATTERN.match(cleaned):
            raise ValueError(
                "El campo 'Ingresos Actuales' solo acepta números positivos (máximo 2 decimales, sin puntos de miles)."
            )
        try:
            income_dec = Decimal(cleaned).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        except InvalidOperation as exc:
            raise ValueError(
                "El campo 'Ingresos Actuales' solo acepta valores numéricos válidos."
            ) from exc

        if income_dec < Decimal(str(MIN_ALLOWED_INCOME)):
            raise ValueError(
                "Los 'Ingresos Actuales' deben ser iguales o superiores a $1.000.000 según la tabla de tarifas."
            )
        if income_dec > Decimal(str(MAX_ALLOWED_INCOME)):
            raise ValueError(
                "Los 'Ingresos Actuales' no pueden superar $1.000.000.000."
            )
        return float(income_dec)

    @staticmethod
    def validate_desired_service(desired_service: str) -> str:
        """Valida que el servicio deseado corresponda a las opciones permitidas."""
        cleaned = desired_service.strip()
        if cleaned not in DESIRED_SERVICES:
            raise ValueError("Debe seleccionar un 'Servicio Deseado' válido.")
        return cleaned

    @staticmethod
    def validate_employment_mode(employment_mode: str) -> str:
        """Valida que la modalidad de empleo sea Empleado o Independiente."""
        cleaned = employment_mode.strip()
        if cleaned not in EMPLOYMENT_MODES:
            raise ValueError(
                "Debe seleccionar una 'Modalidad de Empleo' válida (Empleado o Independiente)."
            )
        return cleaned

    @classmethod
    def validate_affiliation_date(cls, date_text: str) -> str:
        """Valida que la fecha tenga formato dd/mm/aaaa y sea una fecha real entre 1950 y 2100."""
        cleaned = date_text.strip()
        if not cleaned:
            raise ValueError("El campo 'Fecha de Afiliación' es obligatorio.")
        if not cls._STRICT_DATE_PATTERN.match(cleaned):
            raise ValueError(
                "La 'Fecha de Afiliación' debe tener exactamente el formato dd/mm/aaaa (ej. 08/11/2026)."
            )
        try:
            parsed_date = datetime.strptime(cleaned, DATE_FORMAT)
        except ValueError as exc:
            raise ValueError(
                f"La 'Fecha de Afiliación' ({cleaned}) no corresponde a una fecha válida del calendario."
            ) from exc

        if parsed_date.year < MIN_ALLOWED_YEAR or parsed_date.year > MAX_ALLOWED_YEAR:
            raise ValueError(
                f"El año de la 'Fecha de Afiliación' debe estar entre {MIN_ALLOWED_YEAR} y {MAX_ALLOWED_YEAR}."
            )
        return parsed_date.strftime(DATE_FORMAT)

    @staticmethod
    def validate_structure_type(structure_type: str) -> str:
        """Valida que la estructura seleccionada sea Pila, Cola o Lista."""
        cleaned = structure_type.strip()
        if cleaned not in DATA_STRUCTURES:
            raise ValueError(
                "Debe seleccionar una estructura de datos válida (Pila, Cola o Lista)."
            )
        return cleaned

    @classmethod
    def validate_and_create_affiliate(
        cls,
        id_type: str,
        id_number: str,
        full_name: str,
        current_income_text: str,
        desired_service: str,
        employment_mode: str,
        affiliation_date_text: str,
    ) -> Affiliate:
        """Valida todos los campos del formulario, calcula la tarifa y construye el afiliado."""
        validated_id_type = cls.validate_id_type(id_type)
        validated_id_number = cls.validate_id_number(id_number)
        validated_full_name = cls.validate_full_name(full_name)
        validated_income = cls.validate_current_income(current_income_text)
        validated_employment = cls.validate_employment_mode(employment_mode)
        validated_service = cls.validate_desired_service(desired_service)
        validated_date = cls.validate_affiliation_date(affiliation_date_text)

        affiliation_fee = FeeCalculatorService.calculate_fee(
            current_income=validated_income,
            employment_mode=validated_employment,
            desired_service=validated_service,
        )

        return Affiliate(
            id_type=validated_id_type,
            id_number=validated_id_number,
            full_name=validated_full_name,
            current_income=validated_income,
            desired_service=validated_service,
            employment_mode=validated_employment,
            affiliation_fee=affiliation_fee,
            affiliation_date=validated_date,
        )
