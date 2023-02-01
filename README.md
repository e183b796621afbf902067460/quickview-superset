# Medici
It's a core framework for interacting with centralized cryptocurrency exchanges. The purpose of the framework is to implement the logic of the certain centralized cryptocurrency exchange. All exchanges inherit the [iCBE](https://github.com/e183b796621afbf902067460/medici/blob/master/medici/interfaces/exchanges/interface.py#L7) logic.

# Installation
```
pip install git+https://github.com/e183b796621afbf902067460/medici.git#egg=medici
```

# Usage
Let's build our first exchange:
```python
from requests.models import Response

from typing import Optional
import hmac
import hashlib
from urllib.parse import urlencode

from medici.interfaces.exchanges.interface import iCBE
from medici.decorators.permission.decorator import permission


class BinanceSpotExchange(iCBE):
    _E = 'https://api.binance.com'
    _ping = '/api/v3/ping'

    def __signature(self, params: dict):
        return hmac.new(self.secret.encode('utf-8'), urlencode(params).replace('%40', '@').encode('utf-8'), hashlib.sha256).hexdigest()

    def __header(self):
        return {'X-MBX-APIKEY': self.api}

    def aggTrades(
            self,
            symbol: str,
            fromId: Optional[int] = None,
            startTime: Optional[int] = None,
            endTime: Optional[int] = None,
            limit: Optional[int] = None
    ) -> Response:
        params: dict = {
            'symbol': symbol,
            'fromId': fromId,
            'startTime': startTime,
            'endTime': endTime,
            'limit': limit
        }

        r = self._r(method='get', url='/api/v3/aggTrades', params=params)
        assert isinstance(r, Response)
        return r
```
The code above is implementation of the [Binance SPOT](https://binance-docs.github.io/apidocs/spot/en/#change-log) exchange.

Example of exchange building:
```python
from c3f1nance.binance.Spot import BinanceSpotExchange


exchange = BinanceSpotExchange()
```

And finally to call needed methods just do it:
```python
agg_trades = exchange.aggTrades(symbol='ETHUSDT')
```
