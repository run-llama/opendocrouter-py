# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["ParseCreateParams", "Document", "DocumentURLDocument", "DocumentInlineDocument", "DocumentUploadDocument"]


class ParseCreateParams(TypedDict, total=False):
    document: Required[Document]
    """A URL, inline base64 data, or an upload."""

    model: Required[str]
    """A model `id` from `GET /v1/models`."""

    cache: bool
    """
    Store the results, encrypted, for 24 hours: `GET /v1/parse/{id}?expand=markdown`
    reads them and `DELETE /v1/parse/{id}` deletes them sooner. Pages your account
    already has stored for the same document, model and `layout` are served from
    them, free. Required for `async`. Defaults to false.
    """

    layout: bool
    """
    Add each ok page's `layout`: its elements, the markdown lines each one spans and
    where it's printed. Adds $0.20 per million tokens to pages whose layout comes
    back. Defaults to false.
    """

    mode: Literal["sync", "async"]
    """
    `sync` parses the document in this request and returns 200 with results for
    every page, up to the model's `max_sync_pages`. `async` returns 202 parses it as
    a job pollable on `GET /v1/parse/<id>`, up to 500 pages. It needs `cache: true`.
    Defaults to `sync`.
    """

    pages: str
    """1-based pages and ranges.

    Defaults to every page. At most the model's `max_sync_pages` in sync mode, 500
    in async mode.
    """


class DocumentURLDocument(TypedDict, total=False):
    url: Required[str]
    """A public URL to fetch, up to 50 MB."""


class DocumentInlineDocument(TypedDict, total=False):
    data: Required[str]
    """The file, base64-encoded."""

    mime_type: Required[Literal["application/pdf", "image/png", "image/jpeg"]]


class DocumentUploadDocument(TypedDict, total=False):
    upload_id: Required[str]
    """An ID obtained from `POST /v1/uploads`."""


Document: TypeAlias = Union[DocumentURLDocument, DocumentInlineDocument, DocumentUploadDocument]
