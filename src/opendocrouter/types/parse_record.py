# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "ParseRecord",
    "Page",
    "PageRecordOkPage",
    "PageRecordOkPageUsage",
    "PageRecordErrorPage",
    "PageRecordErrorPageError",
    "Usage",
]


class PageRecordOkPageUsage(BaseModel):
    input_tokens: int

    output_tokens: int


class PageRecordOkPage(BaseModel):
    cached: bool
    """Served from the result cache, free."""

    charge_usd: float

    page: int

    status: Literal["ok"]

    usage: PageRecordOkPageUsage

    layout: Optional[object] = None
    """With `expand=layout`, for requests sent with `layout: true`."""

    markdown: Optional[str] = None
    """With `expand=markdown` only."""


class PageRecordErrorPageError(BaseModel):
    code: Literal[
        "provider_error",
        "rate_limited",
        "timeout",
        "output_truncated",
        "content_filtered",
        "repetitive_output",
        "invalid_output",
        "empty_output",
        "at_capacity",
        "unreadable_page",
        "response_too_large",
        "not_processed",
    ]
    """
    - `provider_error`: The provider returned an error.
    - `rate_limited`: The provider rate-limited the page.
    - `timeout`: The page didn't finish before the deadline.
    - `output_truncated`: The output hit the token limit.
    - `content_filtered`: The provider blocked the output, or the model declined.
    - `repetitive_output`: The model got stuck repeating the same text.
    - `invalid_output`: The model answered without transcribing the page.
    - `empty_output`: The model returned no text.
    - `at_capacity`: No provider capacity before the deadline.
    - `unreadable_page`: The PDF opened, but this page couldn't be split or
      rendered.
    - `response_too_large`: The page didn't fit in the response. Request it on its
      own with pages.
    - `not_processed`: The async job ended before this page ran.
    """

    message: str
    """With `expand=markdown`, the page's own message.

    Otherwise the code's standard description.
    """

    reason: Optional[str] = None
    """The provider's own reason when it gave one, e.g.

    `RECITATION`, `SAFETY`, `refusal`, `max_tokens` or `repetition`.
    """


class PageRecordErrorPage(BaseModel):
    charge_usd: Literal[0]

    error: PageRecordErrorPageError

    page: int

    status: Literal["error"]


Page: TypeAlias = Annotated[Union[PageRecordOkPage, PageRecordErrorPage], PropertyInfo(discriminator="status")]


class Usage(BaseModel):
    """Null until the request settles."""

    input_tokens: int

    output_tokens: int

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class ParseRecord(BaseModel):
    id: str
    """For `GET /v1/parse/{id}`."""

    charge_usd: Optional[float] = None
    """Null until the request settles."""

    created_at: datetime

    error_code: Optional[str] = None
    """Why a rejected or failed request ended, as an error code."""

    has_more: bool

    mode: Literal["sync", "async"]
    """The request's `mode`.

    `async` markdown is stored for `expand=markdown`; `sync` markdown is only in the
    POST response.
    """

    model: str

    api_model_version: str = FieldInfo(alias="model_version")

    next_cursor: Optional[int] = None
    """Pass as `cursor` to get the next pages."""

    page_count: int

    pages: List[Page]
    """Empty while processing."""

    pages_done: int

    price_version: str

    results_expire_at: datetime
    """When an async request's stored results are, or were, deleted.

    Null for sync requests, and while processing.
    """

    status: Literal["processing", "completed", "partial", "failed", "expired", "rejected"]
    """`expired`: the request's hold ran out before it settled, so it's free.

    `rejected`: refused before it started (see `error_code`), and free.
    """

    usage: Usage
    """Null until the request settles."""

    poll_url: Optional[str] = None
    """In the 202 response only."""
