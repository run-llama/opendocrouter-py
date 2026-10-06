# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import (
    is_given,
    is_mapping_t,
    get_async_library,
)
from ._compat import cached_property
from ._models import SecurityOptions
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError, OpenDocRouterError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

if TYPE_CHECKING:
    from .resources import parse, models, credits, uploads
    from .resources.parse import ParseResource, AsyncParseResource
    from .resources.models import ModelsResource, AsyncModelsResource
    from .resources.credits import CreditsResource, AsyncCreditsResource
    from .resources.uploads import UploadsResource, AsyncUploadsResource

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "OpenDocRouter",
    "AsyncOpenDocRouter",
    "Client",
    "AsyncClient",
]


class OpenDocRouter(SyncAPIClient):
    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous OpenDocRouter client instance.

        This automatically infers the `api_key` argument from the `OPEN_DOC_ROUTER_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("OPEN_DOC_ROUTER_API_KEY")
        if api_key is None:
            raise OpenDocRouterError(
                "The api_key client option must be set either by passing api_key to the client or by setting the OPEN_DOC_ROUTER_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("OPEN_DOC_ROUTER_BASE_URL")
        if base_url is None:
            base_url = f"https://www.opendocrouter.ai"

        custom_headers_env = os.environ.get("OPEN_DOC_ROUTER_CUSTOM_HEADERS")
        if custom_headers_env is not None:
            parsed: dict[str, str] = {}
            for line in custom_headers_env.split("\n"):
                colon = line.find(":")
                if colon >= 0:
                    parsed[line[:colon].strip()] = line[colon + 1 :].strip()
            default_headers = {**parsed, **(default_headers if is_mapping_t(default_headers) else {})}

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def parse(self) -> ParseResource:
        """Parse documents, synchronously or as async jobs."""
        from .resources.parse import ParseResource

        return ParseResource(self)

    @cached_property
    def uploads(self) -> UploadsResource:
        """Upload documents too large to send inline."""
        from .resources.uploads import UploadsResource

        return UploadsResource(self)

    @cached_property
    def credits(self) -> CreditsResource:
        """Credit, and what each request did and cost."""
        from .resources.credits import CreditsResource

        return CreditsResource(self)

    @cached_property
    def models(self) -> ModelsResource:
        """The models you can parse with, and their prices."""
        from .resources.models import ModelsResource

        return ModelsResource(self)

    @cached_property
    def with_raw_response(self) -> OpenDocRouterWithRawResponse:
        return OpenDocRouterWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OpenDocRouterWithStreamedResponse:
        return OpenDocRouterWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="repeat")

    @override
    def _auth_headers(self, security: SecurityOptions) -> dict[str, str]:
        return {
            **(self._api_key if security.get("api_key", False) else {}),
        }

    @property
    def _api_key(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncOpenDocRouter(AsyncAPIClient):
    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncOpenDocRouter client instance.

        This automatically infers the `api_key` argument from the `OPEN_DOC_ROUTER_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("OPEN_DOC_ROUTER_API_KEY")
        if api_key is None:
            raise OpenDocRouterError(
                "The api_key client option must be set either by passing api_key to the client or by setting the OPEN_DOC_ROUTER_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("OPEN_DOC_ROUTER_BASE_URL")
        if base_url is None:
            base_url = f"https://www.opendocrouter.ai"

        custom_headers_env = os.environ.get("OPEN_DOC_ROUTER_CUSTOM_HEADERS")
        if custom_headers_env is not None:
            parsed: dict[str, str] = {}
            for line in custom_headers_env.split("\n"):
                colon = line.find(":")
                if colon >= 0:
                    parsed[line[:colon].strip()] = line[colon + 1 :].strip()
            default_headers = {**parsed, **(default_headers if is_mapping_t(default_headers) else {})}

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def parse(self) -> AsyncParseResource:
        """Parse documents, synchronously or as async jobs."""
        from .resources.parse import AsyncParseResource

        return AsyncParseResource(self)

    @cached_property
    def uploads(self) -> AsyncUploadsResource:
        """Upload documents too large to send inline."""
        from .resources.uploads import AsyncUploadsResource

        return AsyncUploadsResource(self)

    @cached_property
    def credits(self) -> AsyncCreditsResource:
        """Credit, and what each request did and cost."""
        from .resources.credits import AsyncCreditsResource

        return AsyncCreditsResource(self)

    @cached_property
    def models(self) -> AsyncModelsResource:
        """The models you can parse with, and their prices."""
        from .resources.models import AsyncModelsResource

        return AsyncModelsResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncOpenDocRouterWithRawResponse:
        return AsyncOpenDocRouterWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOpenDocRouterWithStreamedResponse:
        return AsyncOpenDocRouterWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="repeat")

    @override
    def _auth_headers(self, security: SecurityOptions) -> dict[str, str]:
        return {
            **(self._api_key if security.get("api_key", False) else {}),
        }

    @property
    def _api_key(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class OpenDocRouterWithRawResponse:
    _client: OpenDocRouter

    def __init__(self, client: OpenDocRouter) -> None:
        self._client = client

    @cached_property
    def parse(self) -> parse.ParseResourceWithRawResponse:
        """Parse documents, synchronously or as async jobs."""
        from .resources.parse import ParseResourceWithRawResponse

        return ParseResourceWithRawResponse(self._client.parse)

    @cached_property
    def uploads(self) -> uploads.UploadsResourceWithRawResponse:
        """Upload documents too large to send inline."""
        from .resources.uploads import UploadsResourceWithRawResponse

        return UploadsResourceWithRawResponse(self._client.uploads)

    @cached_property
    def credits(self) -> credits.CreditsResourceWithRawResponse:
        """Credit, and what each request did and cost."""
        from .resources.credits import CreditsResourceWithRawResponse

        return CreditsResourceWithRawResponse(self._client.credits)

    @cached_property
    def models(self) -> models.ModelsResourceWithRawResponse:
        """The models you can parse with, and their prices."""
        from .resources.models import ModelsResourceWithRawResponse

        return ModelsResourceWithRawResponse(self._client.models)


class AsyncOpenDocRouterWithRawResponse:
    _client: AsyncOpenDocRouter

    def __init__(self, client: AsyncOpenDocRouter) -> None:
        self._client = client

    @cached_property
    def parse(self) -> parse.AsyncParseResourceWithRawResponse:
        """Parse documents, synchronously or as async jobs."""
        from .resources.parse import AsyncParseResourceWithRawResponse

        return AsyncParseResourceWithRawResponse(self._client.parse)

    @cached_property
    def uploads(self) -> uploads.AsyncUploadsResourceWithRawResponse:
        """Upload documents too large to send inline."""
        from .resources.uploads import AsyncUploadsResourceWithRawResponse

        return AsyncUploadsResourceWithRawResponse(self._client.uploads)

    @cached_property
    def credits(self) -> credits.AsyncCreditsResourceWithRawResponse:
        """Credit, and what each request did and cost."""
        from .resources.credits import AsyncCreditsResourceWithRawResponse

        return AsyncCreditsResourceWithRawResponse(self._client.credits)

    @cached_property
    def models(self) -> models.AsyncModelsResourceWithRawResponse:
        """The models you can parse with, and their prices."""
        from .resources.models import AsyncModelsResourceWithRawResponse

        return AsyncModelsResourceWithRawResponse(self._client.models)


class OpenDocRouterWithStreamedResponse:
    _client: OpenDocRouter

    def __init__(self, client: OpenDocRouter) -> None:
        self._client = client

    @cached_property
    def parse(self) -> parse.ParseResourceWithStreamingResponse:
        """Parse documents, synchronously or as async jobs."""
        from .resources.parse import ParseResourceWithStreamingResponse

        return ParseResourceWithStreamingResponse(self._client.parse)

    @cached_property
    def uploads(self) -> uploads.UploadsResourceWithStreamingResponse:
        """Upload documents too large to send inline."""
        from .resources.uploads import UploadsResourceWithStreamingResponse

        return UploadsResourceWithStreamingResponse(self._client.uploads)

    @cached_property
    def credits(self) -> credits.CreditsResourceWithStreamingResponse:
        """Credit, and what each request did and cost."""
        from .resources.credits import CreditsResourceWithStreamingResponse

        return CreditsResourceWithStreamingResponse(self._client.credits)

    @cached_property
    def models(self) -> models.ModelsResourceWithStreamingResponse:
        """The models you can parse with, and their prices."""
        from .resources.models import ModelsResourceWithStreamingResponse

        return ModelsResourceWithStreamingResponse(self._client.models)


class AsyncOpenDocRouterWithStreamedResponse:
    _client: AsyncOpenDocRouter

    def __init__(self, client: AsyncOpenDocRouter) -> None:
        self._client = client

    @cached_property
    def parse(self) -> parse.AsyncParseResourceWithStreamingResponse:
        """Parse documents, synchronously or as async jobs."""
        from .resources.parse import AsyncParseResourceWithStreamingResponse

        return AsyncParseResourceWithStreamingResponse(self._client.parse)

    @cached_property
    def uploads(self) -> uploads.AsyncUploadsResourceWithStreamingResponse:
        """Upload documents too large to send inline."""
        from .resources.uploads import AsyncUploadsResourceWithStreamingResponse

        return AsyncUploadsResourceWithStreamingResponse(self._client.uploads)

    @cached_property
    def credits(self) -> credits.AsyncCreditsResourceWithStreamingResponse:
        """Credit, and what each request did and cost."""
        from .resources.credits import AsyncCreditsResourceWithStreamingResponse

        return AsyncCreditsResourceWithStreamingResponse(self._client.credits)

    @cached_property
    def models(self) -> models.AsyncModelsResourceWithStreamingResponse:
        """The models you can parse with, and their prices."""
        from .resources.models import AsyncModelsResourceWithStreamingResponse

        return AsyncModelsResourceWithStreamingResponse(self._client.models)


Client = OpenDocRouter

AsyncClient = AsyncOpenDocRouter
