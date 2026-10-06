# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["Credits"]


class Credits(BaseModel):
    available_usd: float
    """What a new request can use: balance minus reserved."""

    balance_usd: float
    """Everything paid in, minus everything charged."""

    reserved_usd: float
    """Held by requests still running."""
