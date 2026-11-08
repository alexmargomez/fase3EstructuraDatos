"""Constantes globales y configuración del sistema Compensándote."""

from typing import Final, Tuple

# Metadatos académicos (UNAD - Anexo 2 Fase 3)
COURSE_NAME: Final[str] = "Estructura de Datos"
COURSE_CODE: Final[str] = "301305"
STUDENT_NAME: Final[str] = "Fabio Alexmar Gomez Sanmiguel"
COLLABORATIVE_GROUP: Final[str] = "301305_93"
UNIVERSITY_INFO: Final[str] = "UNAD · ECBTI · Ingeniería de Sistemas"
PROJECT_NAME: Final[str] = "Fase3FabioGomez"
APPLICATION_DATE: Final[str] = "08/11/2026"

# Clave de acceso estática (RF-01)
STATIC_ACCESS_PASSWORD: Final[str] = "Caja"

# Títulos de ventanas según guía
LOGIN_WINDOW_TITLE: Final[str] = "Login - Compensándote"
MAIN_WINDOW_TITLE: Final[str] = "Caja Compensándote – Control de Afiliados"
ABOUT_WINDOW_TITLE: Final[str] = "Acerca de - Compensándote"

# Opciones de dominio (RF-02 a RF-04)
ID_TYPES: Final[Tuple[str, ...]] = ("CC", "CE", "NUIP", "PAS")

EMPLOYMENT_EMPLOYEE: Final[str] = "Empleado"
EMPLOYMENT_INDEPENDENT: Final[str] = "Independiente"
EMPLOYMENT_MODES: Final[Tuple[str, ...]] = (
    EMPLOYMENT_EMPLOYEE,
    EMPLOYMENT_INDEPENDENT,
)

SERVICE_UNEMPLOYMENT_SUBSIDY: Final[str] = "Subsidio de desempleo"
SERVICE_PARK_ENTRY: Final[str] = "Ingreso a parque"
SERVICE_TRAINING_COURSE: Final[str] = "Curso de formación"
SERVICE_TRAVEL_PACKAGE: Final[str] = "Paquete de viaje"
SERVICE_PREVENTIVE_MEDICINE: Final[str] = "Medicina preventiva"

DESIRED_SERVICES: Final[Tuple[str, ...]] = (
    SERVICE_UNEMPLOYMENT_SUBSIDY,
    SERVICE_PARK_ENTRY,
    SERVICE_TRAINING_COURSE,
    SERVICE_TRAVEL_PACKAGE,
    SERVICE_PREVENTIVE_MEDICINE,
)

STRUCTURE_STACK: Final[str] = "Pila"
STRUCTURE_QUEUE: Final[str] = "Cola"
STRUCTURE_LIST: Final[str] = "Lista"

DATA_STRUCTURES: Final[Tuple[str, ...]] = (
    STRUCTURE_STACK,
    STRUCTURE_QUEUE,
    STRUCTURE_LIST,
)

# Límites de validación y topes de ingresos (Tablas 2 y 3)
MIN_ID_LENGTH: Final[int] = 1
MAX_ID_LENGTH: Final[int] = 15
MIN_NAME_LENGTH: Final[int] = 2
MAX_NAME_LENGTH: Final[int] = 80

MIN_ALLOWED_INCOME: Final[float] = 1_000_000.0
MAX_ALLOWED_INCOME: Final[float] = 1_000_000_000.0
INCOME_TIER_1_MAX: Final[float] = 2_000_000.0
INCOME_TIER_2_MAX: Final[float] = 3_000_000.0
INCOME_TIER_3_MAX: Final[float] = 4_000_000.0
INCOME_TIER_4_MAX: Final[float] = 5_000_000.0

MIN_ALLOWED_YEAR: Final[int] = 1950
MAX_ALLOWED_YEAR: Final[int] = 2100
DATE_FORMAT: Final[str] = "%d/%m/%Y"
