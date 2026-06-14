from time import sleep
from typing import Any, Optional
from urllib.parse import urlencode, urljoin

from httpx import Client, ConnectError, ReadTimeout, RemoteProtocolError, Timeout, get
from pydantic import validate_call


class RestAPI:

    def __init__(self, url: str, default_fields: dict = {}):
        """
        Parameters
        ----------
        url : str
            The base URL for the API
        default_fields : dict
            Query-value parameters to include in every request by default
        """
        self.url = url
        self.default_fields = default_fields
        self._client: Optional[Client] = None

    @validate_call
    def get(
        self,
        endpoint: Optional[str] = None,
        require_defaults: bool = True,
        encode_params: Optional[dict] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Perform a get request to the provided endpoint.

        Parameters
        ----------
        endpoint : str
            The path to the requested resource
        require_defaults : bool
            Inject `default_fields` as query parameters. Default ``True``
        encode_params : dict, optional
            Extra parameters forwarded to ``urlencode``
        kwargs : Any
            Query parameters to include in the request

        Examples
        --------
        api = RestAPI("https://api.com")
        api.get(endpoint="resource", query=1, query2="ABC")
        """
        if require_defaults:
            kwargs.update(self.default_fields)
        query = urlencode(
            {k: v for k, v in kwargs.items() if v is not None},
            **(encode_params or {}),
        )
        path = urljoin(self.url, endpoint)
        req_base_timeout = 10
        req_tries = 3
        req_duration_multiplier = 3
        timeout = Timeout(30.0, connect=30.0, read=30.0, write=30.0)

        while req_tries > 0:
            try:
                request_url = self._urlbuild(path, query)
                if self._client is not None:
                    response = self._client.get(request_url, timeout=timeout)
                else:
                    response = get(request_url, timeout=timeout)
                return response.json()
            except (ReadTimeout, RemoteProtocolError, ConnectError):
                timeout_sec = req_base_timeout * (
                    req_duration_multiplier ** (3 - req_tries)
                )
                print(f"Request timed out. Retrying in {timeout_sec} seconds...")
                sleep(timeout_sec)
                req_tries -= 1

    @staticmethod
    def _urlbuild(
        url: str, query: Optional[str] = None, trailing_slash: bool = False
    ) -> str:
        """
        Build the full url.

        Parameters
        ----------
        url : str
            The URL to build from
        query : str, optional
            URL-encoded query string to append
        trailing_slash : bool
            Preserve trailing slash on the URL. Default ``False``
        """
        if (url[-1] == "/") and not trailing_slash:
            url = url[:-1]

        if query:
            return f"{url}?{query}"
        else:
            return url

    def __enter__(self) -> "RestAPI":
        self._client = Client()
        return self

    def __exit__(self, *exc_info: Any) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
