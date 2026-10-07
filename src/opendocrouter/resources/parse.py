# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import parse_get_params, parse_create_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.parse_record import ParseRecord
from ..types.parse_delete_response import ParseDeleteResponse

__all__ = ["ParseResource", "AsyncParseResource"]


class ParseResource(SyncAPIResource):
    """
    Parse documents, synchronously (up to 50 pages) or as async jobs (up to 500 pages).
    """

    @cached_property
    def with_raw_response(self) -> ParseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/run-llama/opendocrouter-python#accessing-raw-response-data-eg-headers
        """
        return ParseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ParseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/run-llama/opendocrouter-python#with_streaming_response
        """
        return ParseResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        document: parse_create_params.Document,
        model: str,
        cache: bool | Omit = omit,
        layout: bool | Omit = omit,
        mode: Literal["sync", "async"] | Omit = omit,
        pages: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParseRecord:
        """
        `mode: "sync"` (the default) parses the document in this request and returns 200
        with every page, up to the model's `max_sync_pages`. `mode: "async"`, which
        needs `cache: true`, returns 202 and parses up to 500 pages as a job;
        `GET /v1/parse/{id}?expand=markdown` has the results. At most 5 async requests
        run at once per account, and at most 300 requests a minute.

        Admission holds the most the request could cost; it's released, less the actual
        charge, when the request finishes. Failed pages are free.

        Args:
          document: A URL, inline base64 data, or an upload.

          model: A model `id` from `GET /v1/models`.

          cache: Store the results, encrypted, for 24 hours: `GET /v1/parse/{id}?expand=markdown`
              reads them and `DELETE /v1/parse/{id}` deletes them sooner. Pages your account
              already has stored for the same document, model and `layout` are served from
              them, free. Required for `async`. Defaults to false.

          layout: Add each ok page's `layout`: its elements, the markdown lines each one spans and
              where it's printed. Adds $0.20 per million tokens to pages whose layout comes
              back. Defaults to false.

          mode: `sync` parses the document in this request and returns 200 with results for
              every page, up to the model's `max_sync_pages`. `async` returns 202 parses it as
              a job pollable on `GET /v1/parse/<id>`, up to 500 pages. It needs `cache: true`.
              Defaults to `sync`.

          pages: 1-based pages and ranges. Defaults to every page. At most the model's
              `max_sync_pages` in sync mode, 500 in async mode.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/parse",
            body=maybe_transform(
                {
                    "document": document,
                    "model": model,
                    "cache": cache,
                    "layout": layout,
                    "mode": mode,
                    "pages": pages,
                },
                parse_create_params.ParseCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParseRecord,
        )

    def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParseDeleteResponse:
        """
        Deletes the results stored with `cache: true`, so they're also no longer served
        from the cache. A running job stops before its next chunk. Pages already parsed
        are still charged. The request's status and cost stay available.

        Args:
          id: The parse request's `id`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._delete(
            path_template("/v1/parse/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParseDeleteResponse,
        )

    def get(
        self,
        id: str,
        *,
        cursor: int | Omit = omit,
        expand: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParseRecord:
        """Works for any request.

        While it runs, `pages` is empty and `pages_done` counts
        progress. Then it returns every page, unless the expanded results are over 4 MB:
        then `has_more` is true, and you ask again with `cursor` set to `next_cursor`.

        Markdown and layout are opt-in, with `expand`, and only requests sent with
        `cache: true` store them, for 24 hours after they finish. Without `expand`, this
        never returns document text.

        Args:
          id: The parse request's `id`.

          cursor: The `next_cursor` of the previous response.

          expand: `markdown` adds each ok page's markdown, `layout` its layout (for requests sent
              with `layout: true`), and `markdown,layout` both. For requests sent with
              `cache: true`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/v1/parse/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "expand": expand,
                    },
                    parse_get_params.ParseGetParams,
                ),
            ),
            cast_to=ParseRecord,
        )


class AsyncParseResource(AsyncAPIResource):
    """
    Parse documents, synchronously (up to 50 pages) or as async jobs (up to 500 pages).
    """

    @cached_property
    def with_raw_response(self) -> AsyncParseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/run-llama/opendocrouter-python#accessing-raw-response-data-eg-headers
        """
        return AsyncParseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncParseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/run-llama/opendocrouter-python#with_streaming_response
        """
        return AsyncParseResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        document: parse_create_params.Document,
        model: str,
        cache: bool | Omit = omit,
        layout: bool | Omit = omit,
        mode: Literal["sync", "async"] | Omit = omit,
        pages: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParseRecord:
        """
        `mode: "sync"` (the default) parses the document in this request and returns 200
        with every page, up to the model's `max_sync_pages`. `mode: "async"`, which
        needs `cache: true`, returns 202 and parses up to 500 pages as a job;
        `GET /v1/parse/{id}?expand=markdown` has the results. At most 5 async requests
        run at once per account, and at most 300 requests a minute.

        Admission holds the most the request could cost; it's released, less the actual
        charge, when the request finishes. Failed pages are free.

        Args:
          document: A URL, inline base64 data, or an upload.

          model: A model `id` from `GET /v1/models`.

          cache: Store the results, encrypted, for 24 hours: `GET /v1/parse/{id}?expand=markdown`
              reads them and `DELETE /v1/parse/{id}` deletes them sooner. Pages your account
              already has stored for the same document, model and `layout` are served from
              them, free. Required for `async`. Defaults to false.

          layout: Add each ok page's `layout`: its elements, the markdown lines each one spans and
              where it's printed. Adds $0.20 per million tokens to pages whose layout comes
              back. Defaults to false.

          mode: `sync` parses the document in this request and returns 200 with results for
              every page, up to the model's `max_sync_pages`. `async` returns 202 parses it as
              a job pollable on `GET /v1/parse/<id>`, up to 500 pages. It needs `cache: true`.
              Defaults to `sync`.

          pages: 1-based pages and ranges. Defaults to every page. At most the model's
              `max_sync_pages` in sync mode, 500 in async mode.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/parse",
            body=await async_maybe_transform(
                {
                    "document": document,
                    "model": model,
                    "cache": cache,
                    "layout": layout,
                    "mode": mode,
                    "pages": pages,
                },
                parse_create_params.ParseCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParseRecord,
        )

    async def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParseDeleteResponse:
        """
        Deletes the results stored with `cache: true`, so they're also no longer served
        from the cache. A running job stops before its next chunk. Pages already parsed
        are still charged. The request's status and cost stay available.

        Args:
          id: The parse request's `id`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._delete(
            path_template("/v1/parse/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParseDeleteResponse,
        )

    async def get(
        self,
        id: str,
        *,
        cursor: int | Omit = omit,
        expand: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParseRecord:
        """Works for any request.

        While it runs, `pages` is empty and `pages_done` counts
        progress. Then it returns every page, unless the expanded results are over 4 MB:
        then `has_more` is true, and you ask again with `cursor` set to `next_cursor`.

        Markdown and layout are opt-in, with `expand`, and only requests sent with
        `cache: true` store them, for 24 hours after they finish. Without `expand`, this
        never returns document text.

        Args:
          id: The parse request's `id`.

          cursor: The `next_cursor` of the previous response.

          expand: `markdown` adds each ok page's markdown, `layout` its layout (for requests sent
              with `layout: true`), and `markdown,layout` both. For requests sent with
              `cache: true`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/v1/parse/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "cursor": cursor,
                        "expand": expand,
                    },
                    parse_get_params.ParseGetParams,
                ),
            ),
            cast_to=ParseRecord,
        )


class ParseResourceWithRawResponse:
    def __init__(self, parse: ParseResource) -> None:
        self._parse = parse

        self.create = to_raw_response_wrapper(
            parse.create,
        )
        self.delete = to_raw_response_wrapper(
            parse.delete,
        )
        self.get = to_raw_response_wrapper(
            parse.get,
        )


class AsyncParseResourceWithRawResponse:
    def __init__(self, parse: AsyncParseResource) -> None:
        self._parse = parse

        self.create = async_to_raw_response_wrapper(
            parse.create,
        )
        self.delete = async_to_raw_response_wrapper(
            parse.delete,
        )
        self.get = async_to_raw_response_wrapper(
            parse.get,
        )


class ParseResourceWithStreamingResponse:
    def __init__(self, parse: ParseResource) -> None:
        self._parse = parse

        self.create = to_streamed_response_wrapper(
            parse.create,
        )
        self.delete = to_streamed_response_wrapper(
            parse.delete,
        )
        self.get = to_streamed_response_wrapper(
            parse.get,
        )


class AsyncParseResourceWithStreamingResponse:
    def __init__(self, parse: AsyncParseResource) -> None:
        self._parse = parse

        self.create = async_to_streamed_response_wrapper(
            parse.create,
        )
        self.delete = async_to_streamed_response_wrapper(
            parse.delete,
        )
        self.get = async_to_streamed_response_wrapper(
            parse.get,
        )
