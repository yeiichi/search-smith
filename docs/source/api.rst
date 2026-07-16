API Reference
=============

``search_smith.search``
-----------------------

.. code-block:: python

   search(
       query: str,
       *,
       count: int = 10,
       offset: int = 0,
       provider: SearchProvider | None = None,
   ) -> list[SearchResult]

Runs a web search. If no provider is passed, Brave Search is used.

``BraveSearch``
---------------

.. code-block:: python

   BraveSearch(
       api_key: str | None = None,
       *,
       timeout: float = 10.0,
       client: httpx.Client | None = None,
   )

``BraveSearch.search()`` accepts ``query``, ``count``, and ``offset``, then
returns provider-neutral ``SearchResult`` objects in Brave ranking order.

An injected ``httpx.Client`` is useful for tests and custom application
transport configuration.

``SearchResult``
----------------

Fields:

* ``title: str``
* ``url: str``
* ``snippet: str``
* ``source: str``
* ``rank: int``
* ``score: float | None``
* ``metadata: Mapping[str, Any]``

The dataclass is frozen and uses slots. Invalid empty title, URL, source,
negative score, or rank below 1 raises ``ValueError``.

Exceptions
----------

All package-specific exceptions inherit from ``SearchSmithError``.

* ``ConfigurationError``: required configuration is missing.
* ``AuthenticationError``: provider rejected credentials.
* ``RateLimitError``: provider rate limit was reached.
* ``ProviderError``: provider, network, or response parsing failure.

Provider Architecture
---------------------

Providers implement a small protocol:

.. code-block:: python

   provider.search(query, *, count=10, offset=0) -> list[SearchResult]

Future providers should normalize their own native responses into
``SearchResult`` and preserve useful provider-specific data in ``metadata``.
