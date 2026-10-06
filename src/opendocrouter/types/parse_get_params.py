# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ParseGetParams"]


class ParseGetParams(TypedDict, total=False):
    cursor: int
    """The `next_cursor` of the previous response."""

    expand: str
    """
    `markdown` adds each ok page's markdown, `layout` its layout (for requests sent
    with `layout: true`), and `markdown,layout` both. Async requests only.
    """
