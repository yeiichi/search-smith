Usage
=====

Python API
----------

.. code-block:: python

   from search_smith import search

   results = search("Python semantic release", count=10)

   for result in results:
       print(result.title)
       print(result.url)
       print(result.snippet)

Explicit Brave Client
---------------------

.. code-block:: python

   from search_smith import BraveSearch

   with BraveSearch() as client:
       results = client.search("Brave Search API", count=5)

Constructor arguments take precedence over environment variables. Use this when
your application has already loaded the secret from a safe runtime source:

.. code-block:: python

   import os

   client = BraveSearch(api_key=os.environ["BRAVE_SEARCH_API_KEY"])

CLI
---

.. code-block:: bash

   search-smith "Python semantic release"
   search-smith "Cretan fact checking" --count 5
   search-smith "Brave Search API" --format json

Text output is meant for terminals. JSON output is a stable list of normalized
result objects.

Result Model
------------

Each result is a ``SearchResult``:

.. code-block:: python

   SearchResult(
       title="Example",
       url="https://example.com",
       snippet="Short result excerpt.",
       source="brave",
       rank=1,
       score=None,
       metadata={},
   )

``metadata`` preserves useful provider-specific fields that are not part of the
provider-neutral model.
