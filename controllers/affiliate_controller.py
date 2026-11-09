"""Controller encapsulating validation, fee calculation, and linear structure operations."""

from datetime import datetime
import re
from typing import List as PyList, Optional

from models.affiliate import Affiliate
from models.structures import AffiliateList, AffiliateQueue, AffiliateStack

# Academic and domain constants
COURSE_NAME = "Estructura de Datos"
COURSE_CODE = "301305"
STUDENT_NAME = "Fabio Alexmar Gomez Sanmiguel"
COLLABORATIVE_GROUP = "301305_93"
UNIVERSITY_INFO = "UNAD · ECBTI · Ingeniería de Sistemas"
PROJECT_NAME = "Fase3FabioGomez"
APPLICATION_DATE = "09/11/2026"

ACCESS_PASSWORD = "Caja"

ID_TYPES = ("CC", "CE", "NUIP", "PAS")
EMPLOYMENT_MODES = ("Empleado", "Independiente")
DESIRED_SERVICES = (
    "Subsidio de desempleo",
    "Ingreso a parque",
    "Curso de formación",
    "Paquete de viaje",
    "Medicina preventiva",
)
DATA_STRUCTURES = ("Pila", "Cola", "Lista")


class AffiliateController:
    """Coordinates business rules, fee calculation, validation, and linear structures."""

    _NAME_PATTERN = re.compile(
        r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü]+(?: [A-Za-zÁÉÍÓÚáéíóúÑñÜü]+)*$"
    )
    _REALTIME_ALPHA_PATTERN = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]*$")
    _REALTIME_NUMBER_PATTERN = re.compile(r"^(?:[0-9]+(?:\.[0-9]{0,2})?)?$")

    def __init__(self) -> None:
        self.stack = AffiliateStack()
        self.queue = AffiliateQueue()
        self.affiliate_list = AffiliateList()

    @staticmethod
    def validate_password(password: str) -> bool:
        """Validates whether the entered password matches 'Caja'."""
        return password == ACCESS_PASSWORD

    @staticmethod
    def is_valid_key_digits(text: str) -> bool:
        """Keyboard filter allowing only ASCII digits up to 15 characters."""
        return text == "" or (text.isascii() and text.isdigit() and len(text) <= 15)

    @classmethod
    def is_valid_key_letters(cls, text: str) -> bool:
        """Keyboard filter allowing only alphabetic characters and spaces."""
        return len(text) <= 80 and bool(cls._REALTIME_ALPHA_PATTERN.match(text))

    @classmethod
    def is_valid_key_income(cls, text: str) -> bool:
        """Keyboard filter allowing only positive numeric values."""
        return len(text) <= 15 and bool(cls._REALTIME_NUMBER_PATTERN.match(text))

    @staticmethod
    def calculate_fee(
        current_income: float,
        employment_mode: str,
        desired_service: str,
    ) -> float:
        """Calculates the affiliation fee according to Tables 2 and 3 and service surcharges."""
        if current_income < 1_000_000.0:
            raise ValueError(
                "Los 'Ingresos Actuales' deben ser iguales o superiores a $1.000.000 según la tabla de tarifas."
            )

        # Table 2 (Empleado) and Table 3 (Independiente)
        if employment_mode == "Empleado":
            if current_income <= 2_000_000.0:
                base_fee = 45_000.0
            elif current_income <= 3_000_000.0:
                base_fee = 60_000.0
            elif current_income <= 4_000_000.0:
                base_fee = 75_000.0
            elif current_income <= 5_000_000.0:
                base_fee = 90_000.0
            else:
                base_fee = 150_000.0
        elif employment_mode == "Independiente":
            if current_income <= 2_000_000.0:
                base_fee = 10_000.0
            elif current_income <= 3_000_000.0:
                base_fee = 20_000.0
            elif current_income <= 4_000_000.0:
                base_fee = 30_000.0
            elif current_income <= 5_000_000.0:
                base_fee = 40_000.0
            else:
                base_fee = 80_000.0
        else:
            raise ValueError(f"Modalidad de empleo no válida: '{employment_mode}'.")

        # Surcharge by desired service
        if desired_service == "Subsidio de desempleo":
            surcharge = 0.0
        elif desired_service == "Ingreso a parque":
            surcharge = 2_500.0
        elif desired_service == "Curso de formación":
            surcharge = 7_500.0
        elif desired_service == "Paquete de viaje":
            surcharge = 10_000.0
        elif desired_service == "Medicina preventiva":
            surcharge = round(current_income * 0.10, 2)
        else:
            raise ValueError(f"Servicio deseado no válido: '{desired_service}'.")

        return round(base_fee + surcharge, 2)

    @classmethod
    def create_affiliate(
        cls,
        id_type: str,
        id_number: str,
        full_name: str,
        current_income_text: str,
        desired_service: str,
        employment_mode: str,
        affiliation_date_text: str,
    ) -> Affiliate:
        """Validates all form inputs, computes the fee, and returns an Affiliate instance."""
        clean_id_type = id_type.strip()
        clean_id_number = id_number.strip()
        clean_name = " ".join(full_name.strip().split())
        clean_income_text = current_income_text.strip()
        clean_service = desired_service.strip()
        clean_employment = employment_mode.strip()
        clean_date = affiliation_date_text.strip()

        if clean_id_type not in ID_TYPES:
            raise ValueError("Debe seleccionar un Tipo de Identificación válido.")
        if not clean_id_number or not clean_id_number.isdigit() or int(clean_id_number) == 0:
            raise ValueError(
                "El campo 'Número de Identificación' es obligatorio y solo acepta números."
            )
        if not clean_name or len(clean_name) < 2 or not cls._NAME_PATTERN.match(clean_name):
            raise ValueError(
                "El campo 'Nombre Completo' es obligatorio y solo acepta letras."
            )
        if not clean_income_text:
            raise ValueError("El campo 'Ingresos Actuales' es obligatorio.")
        try:
            current_income = float(clean_income_text)
        except ValueError as exc:
            raise ValueError(
                "El campo 'Ingresos Actuales' solo acepta valores numéricos."
            ) from exc

        try:
            parsed_date = datetime.strptime(clean_date, "%d/%m/%Y")
            if parsed_date.year < 1950 or parsed_date.year > 2100:
                raise ValueError
            formatted_date = parsed_date.strftime("%d/%m/%Y")
        except ValueError as exc:
            raise ValueError(
                "La 'Fecha de Afiliación' debe ser una fecha real en formato dd/mm/aaaa."
            ) from exc

        fee = cls.calculate_fee(current_income, clean_employment, clean_service)
        return Affiliate(
            id_type=clean_id_type,
            id_number=clean_id_number,
            full_name=clean_name,
            current_income=current_income,
            desired_service=clean_service,
            employment_mode=clean_employment,
            affiliation_fee=fee,
            affiliation_date=formatted_date,
        )

    def register_affiliate(self, structure_type: str, affiliate: Affiliate) -> None:
        """Inserts an affiliate into the selected linear structure (Pila, Cola, or Lista)."""
        if structure_type == "Pila":
            self.stack.push(affiliate)
        elif structure_type == "Cola":
            self.queue.enqueue(affiliate)
        elif structure_type == "Lista":
            self.affiliate_list.add(affiliate)
        else:
            raise ValueError(f"Estructura no válida: '{structure_type}'.")

    def get_records(self, structure_type: str) -> PyList[Affiliate]:
        """Returns the current records of the selected structure."""
        if structure_type == "Pila":
            return self.stack.get_all()
        if structure_type == "Cola":
            return self.queue.get_all()
        if structure_type == "Lista":
            return self.affiliate_list.get_all()
        raise ValueError(f"Estructura no válida: '{structure_type}'.")

    def peek_for_deletion(
        self,
        structure_type: str,
        target_id: Optional[str] = None,
    ) -> Optional[Affiliate]:
        """Returns the candidate affiliate to be deleted before asking user confirmation."""
        if structure_type == "Pila":
            return self.stack.peek()
        if structure_type == "Cola":
            return self.queue.peek()
        if structure_type == "Lista":
            if not target_id:
                return None
            return self.affiliate_list.find_by_id(target_id)
        raise ValueError(f"Estructura no válida: '{structure_type}'.")

    def delete_affiliate(
        self,
        structure_type: str,
        target_id: Optional[str] = None,
    ) -> Affiliate:
        """Deletes and returns the affiliate according to the selected structure's behavior."""
        if structure_type == "Pila":
            return self.stack.pop()
        if structure_type == "Cola":
            return self.queue.dequeue()
        if structure_type == "Lista":
            if not target_id or not target_id.strip():
                raise ValueError(
                    "Para eliminar en la estructura Lista, debe digitar primero el Número de Identificación del afiliado."
                )
            return self.affiliate_list.remove_by_id(target_id)
        raise ValueError(f"Estructura no válida: '{structure_type}'.")

    def generate_report_text(self, structure_type: str) -> str:
        """Generates the formatted report string for the selected structure."""
        if structure_type == "Pila":
            total_fees = self.stack.get_total_fees()
            return f"Suma de tarifas de afiliación (Pila): ${total_fees:,.2f}"
        if structure_type == "Cola":
            count = self.queue.get_record_count()
            suffix = "registro" if count == 1 else "registros"
            return f"Cantidad de registros en la Cola: {count} {suffix}"
        if structure_type == "Lista":
            avg_income = self.affiliate_list.get_average_income()
            return f"Promedio de ingresos actuales (Lista): ${avg_income:,.2f}"
        raise ValueError(f"Estructura no válida: '{structure_type}'.")
