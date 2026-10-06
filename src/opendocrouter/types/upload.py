# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from .._models import BaseModel

__all__ = ["Upload"]


class Upload(BaseModel):
    expires_at: datetime

    max_bytes: int

    upload_id: str

    upload_url: str
    """PUT the file here."""
