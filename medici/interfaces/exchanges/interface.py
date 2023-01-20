from typing import Dict, Any, Optional, Generic, overload, final
from abc import ABC, abstractmethod

import requests as r


class iCBE(ABC):
    _E = None

    def __init__(self, api: Optional[str] = None, secret: Optional[str] = None, *args, **kwargs) -> None:
        self._api = api
        self._secret = secret

        self.builder.build(
            key='endpoint', value=self.endpoint
        ).build(
            key='api', value=self.api
        ).build(
            key='secret', value=self.secret
        )

    @abstractmethod
    def _r(self):
        raise NotImplemented(f'Request method should be implemented in {__class__.__name__}')

    @property
    def endpoint(self) -> str:
        return self._E

    @property
    def api(self) -> str:
        return self._api

    @property
    def secret(self) -> str:
        return self._secret

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
                    if r.get(url=v).status_code != 200:
                        raise r.HTTPError("Set valid endpoint")
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

    @property
    def builder(self):
        return self.Builder()
