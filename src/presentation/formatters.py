"""Utilidades de formato visual para presentar afiliados en la interfaz gráfica."""

from typing import Tuple

from src.domain.affiliate import Affiliate


def format_currency(amount: float) -> str:
    """Formatea un valor numérico como moneda en pesos."""
    return f"${amount:,.2f}"


def format_affiliate_treeview_row(
    affiliate: Affiliate,
) -> Tuple[str, str, str, str, str, str, str, str]:
    """Convierte una entidad Affiliate en una tupla formateada para el Treeview."""
    return (
        affiliate.id_type,
        affiliate.id_number,
        affiliate.full_name,
        format_currency(affiliate.current_income),
        affiliate.desired_service,
        affiliate.employment_mode,
        format_currency(affiliate.affiliation_fee),
        affiliate.affiliation_date,
    )
