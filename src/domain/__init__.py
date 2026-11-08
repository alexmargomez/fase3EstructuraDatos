"""Exportaciones de la capa de dominio."""

from src.domain.affiliate import (
    Affiliate,
    AffiliateDataStructure,
    EstructuraDatosAfiliado,
)
from src.domain.data_structures import (
    AffiliateList,
    AffiliateQueue,
    AffiliateRepository,
    AffiliateStack,
    BaseAffiliateStructure,
    List,
    Queue,
    Stack,
)

__all__ = [
    "Affiliate",
    "AffiliateDataStructure",
    "EstructuraDatosAfiliado",
    "BaseAffiliateStructure",
    "Stack",
    "Queue",
    "List",
    "AffiliateStack",
    "AffiliateQueue",
    "AffiliateList",
    "AffiliateRepository",
]
