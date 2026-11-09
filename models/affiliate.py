"""Affiliate domain model (EstructuraDatosAfiliado)."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Affiliate:
    """Immutable entity representing an affiliate registered in Memory."""

    id_type: str
    id_number: str
    full_name: str
    current_income: float
    desired_service: str
    employment_mode: str
    affiliation_fee: float
    affiliation_date: str

    def to_treeview_row(self) -> Tuple[str, str, str, str, str, str, str, str]:
        """Returns the affiliate attributes formatted for the GUI Treeview."""
        return (
            self.id_type,
            self.id_number,
            self.full_name,
            f"${self.current_income:,.2f}",
            self.desired_service,
            self.employment_mode,
            f"${self.affiliation_fee:,.2f}",
            self.affiliation_date,
        )


# Alias required by the UNAD Annex 2 guide
EstructuraDatosAfiliado = Affiliate
