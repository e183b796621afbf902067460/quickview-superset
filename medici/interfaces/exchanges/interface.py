from typing import Dict, Any, Optional, Generic, overload, final
from abc import ABC, abstractmethod

import requests as r


class iCBE(ABC):
    _E = None
    _ping = None

    def __init__(self, api: Optional[str] = None, secret: Optional[str] = None, *args, **kwargs) -> None:
        self._api = api
        self._secret = secret

        self.builder.build(
            key='endpoint', value=self.endpoint
        ).build(
            key='api', value=self.api
        ).build(
            key='secret', value=self.secret
        ).build(
            key='ping', value=self.ping
        ).connect()

    @final
    def _r(
            self,
            method: str, url: str,
            params: Optional[dict] = None,
            headers: Optional[dict] = None,
            proxies: Optional[dict] = None
    ):
        if method == 'get':
            return r.get(self.endpoint + url, params=params, headers=headers, proxies=proxies)
        elif method == 'post':
            return r.post(self.endpoint + url, data=params, headers=headers, proxies=proxies)
        elif method == 'delete':
            return r.delete(self.endpoint + url, data=params, headers=headers, proxies=proxies)
        elif method == 'put':
            return r.put(self.endpoint + url, data=params, headers=headers, proxies=proxies)
        raise ConnectionError('Wrong method')

    @property
    def endpoint(self) -> str:
        return self._E

    @property
    def ping(self) -> str:
        return self._ping

    @property
    def api(self) -> str:
        return self._api

    @property
    def secret(self) -> str:
        return self._secret

    @final
    def _validate_response(self, r: r.Response) -> bool:
        return r.status_code == 200

    class Builder:
        def __init__(self) -> None:
            self._options: Dict[str, Any] = dict()

        @overload
        def build(self, params: Dict[str, Any]) -> "iCBE.Builder":
            ...

        @overload
        def build(self, key: str, value: Any) -> "iCBE.Builder":
            ...

        @final
        def build(
                self,
                key: Optional[str] = None,
                value: Optional[str] = None,
                params: Optional[Dict[str, Any]] = None
        ) -> "iCBE.Builder":

            def validate(k: str, v: Any) -> None:
                if k == 'endpoint':
                    if not isinstance(v, str):
                        raise TypeError('Endpoint is not string')
                    if not v.startswith("https:") and not v.startswith("http:"):
                        raise r.HTTPError("Set valid endpoint")
                if k == 'ping':
                    if not isinstance(v, str):
                        raise TypeError('Ping endpoint is not string')
                elif k == 'api':
                    if not isinstance(v, str):
                        if v is not None:
                            raise TypeError("Invalid API key")
                elif k == 'secret':
                    if not isinstance(v, str):
                        if v is not None:
                            raise TypeError("Invalid Secret key")

            if isinstance(params, dict):
                for k, v in params.items():
                    validate(k=k, v=v)
                    self._options[k] = v
            elif isinstance(key, str):
                validate(k=key, v=value)
                self._options[key] = value
            return self

        def connect(self):
            try:
                status = r.get(self._options['endpoint'] + self._options['ping']).status_code
            except KeyError:
                raise TypeError('Set valid ping or endpoint parameter')
            if status != 200:
                raise r.HTTPError('Provider is down')
            return self

    @property
    def builder(self):
        return self.Builder()
