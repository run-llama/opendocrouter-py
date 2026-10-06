# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "ParseResult",
    "Page",
    "PageOkPage",
    "PageOkPageUsage",
    "PageOkPageLayout",
    "PageOkPageLayoutPageLayoutOk",
    "PageOkPageLayoutPageLayoutOkElement",
    "PageOkPageLayoutPageLayoutOkElementBox",
    "PageOkPageLayoutPageLayoutError",
    "PageOkPageLayoutPageLayoutErrorError",
    "PageErrorPage",
    "PageErrorPageError",
    "Usage",
]


class PageOkPageUsage(BaseModel):
    input_tokens: int

    output_tokens: int


class PageOkPageLayoutPageLayoutOkElementBox(BaseModel):
    """Fractions of the page width and height, from the top left."""

    h: float

    w: float

    x: float

    y: float

    r: Optional[float] = None
    """Clockwise degrees about the box's centre, for text printed at an angle.

    x, y, w and h are then the unrotated box.
    """


class PageOkPageLayoutPageLayoutOkElement(BaseModel):
    boxes: List[PageOkPageLayoutPageLayoutOkElementBox]
    """In reading order.

    Empty when the element couldn't be placed; more than one when it's printed in
    pieces, such as a paragraph that continues in the next column.
    """

    confidence: float

    lines: Optional[List[object]] = None
    """
    First and last line of the page markdown, 0-based and inclusive, splitting on
    "\n" only. Null for a picture the markdown doesn't mention.
    """

    type: Literal[
        "title",
        "section_header",
        "text",
        "list_item",
        "table",
        "picture",
        "chart",
        "formula",
        "caption",
        "footnote",
        "page_header",
        "page_footer",
        "code",
        "form",
        "key_value",
    ]


class PageOkPageLayoutPageLayoutOk(BaseModel):
    elements: List[PageOkPageLayoutPageLayoutOkElement]
    """The markdown's elements in reading order, then pictures it doesn't mention."""

    height: float

    status: Literal["ok"]

    width: float
    """Points for a PDF page, pixels for an image."""


class PageOkPageLayoutPageLayoutErrorError(BaseModel):
    code: Literal["provider_error", "timeout", "unreadable_page", "at_capacity"]

    message: str


class PageOkPageLayoutPageLayoutError(BaseModel):
    """The page's markdown is still there; layout isn't charged."""

    error: PageOkPageLayoutPageLayoutErrorError

    status: Literal["error"]


PageOkPageLayout: TypeAlias = Annotated[
    Union[PageOkPageLayoutPageLayoutOk, PageOkPageLayoutPageLayoutError], PropertyInfo(discriminator="status")
]


class PageOkPage(BaseModel):
    cached: bool
    """Served from the result cache, free."""

    charge_usd: float

    markdown: str

    page: int

    status: Literal["ok"]

    usage: PageOkPageUsage

    layout: Optional[PageOkPageLayout] = None
    """With `layout: true` only."""


class PageErrorPageError(BaseModel):
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

    reason: Optional[str] = None
    """The provider's own reason when it gave one, e.g.

    `RECITATION`, `SAFETY`, `refusal`, `max_tokens` or `repetition`.
    """


class PageErrorPage(BaseModel):
    charge_usd: Literal[0]

    error: PageErrorPageError

    page: int

    status: Literal["error"]


Page: TypeAlias = Annotated[Union[PageOkPage, PageErrorPage], PropertyInfo(discriminator="status")]


class Usage(BaseModel):
    input_tokens: int

    output_tokens: int


class ParseResult(BaseModel):
    id: str
    """For `GET /v1/parse/{id}`."""

    charge_usd: float

    model: str

    api_model_version: str = FieldInfo(alias="model_version")

    pages: List[Page]
    """
    There's no joined markdown, to stay under the response size limit: join
    `pages[].markdown` yourself.
    """

    price_version: str

    status: Literal["completed", "partial", "failed"]

    usage: Usage
