# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["ModelListResponse", "Data", "DataPageLatency", "DataParsebench", "DataPricePerMillionTokens"]


class DataPageLatency(BaseModel):
    """
    How long one page takes on this version, from its most recent successful pages (up to 1,000, within 30 days). Pages in a request run in parallel. Null until enough pages are measured.
    """

    p50_seconds: float

    p90_seconds: float


class DataParsebench(BaseModel):
    """ParseBench scores for this version. Null while benchmarking."""

    charts: float

    content_faithfulness: float

    score: float
    """Mean of the five category scores."""

    semantic_formatting: float

    tables: float

    visual_grounding: float
    """How well `layout: true` places each element on the page."""


class DataPricePerMillionTokens(BaseModel):
    cached_input: float

    input: float

    output: float


class Data(BaseModel):
    id: str

    avg_charge_per_page_usd: Optional[float] = None
    """
    What a typical page costs at these prices: the mean tokens per page this version
    used on ParseBench. An estimate; your pages may differ. Null until benchmarked.
    """

    cold_starts: bool
    """True for models on GPUs we start on demand.

    After the model sits idle, a request waits up to 45 seconds for one to start, or
    fails with `model_starting` if it takes longer, without being charged.
    """

    max_charge_per_page_usd: float
    """The most one page can be charged, which is what a request holds per page."""

    max_sync_pages: int
    """Most pages a `mode: "sync"` request can take."""

    name: str

    page_latency: DataPageLatency
    """
    How long one page takes on this version, from its most recent successful pages
    (up to 1,000, within 30 days). Pages in a request run in parallel. Null until
    enough pages are measured.
    """

    parsebench: DataParsebench
    """ParseBench scores for this version. Null while benchmarking."""

    price_per_million_tokens: DataPricePerMillionTokens

    version: str
    """Changes whenever output behavior can change."""


class ModelListResponse(BaseModel):
    data: List[Data]

    price_version: str
