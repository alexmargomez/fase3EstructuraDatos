"""Domain models package: Affiliate entity and linear data structures."""

from models.affiliate import Affiliate, EstructuraDatosAfiliado
from models.structures import (
    AffiliateList,
    AffiliateQueue,
    AffiliateStack,
    BaseLinearStructure,
)

__all__ = [
    "Affiliate",
    "EstructuraDatosAfiliado",
    "BaseLinearStructure",
    "AffiliateStack",
    "AffiliateQueue",
    "AffiliateList",
]
