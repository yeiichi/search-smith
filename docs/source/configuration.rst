Configuration
=============

Brave Search API Key
--------------------

``search-smith`` reads Brave credentials from:

.. code-block:: bash

   BRAVE_SEARCH_API_KEY

You can also pass an API key directly when your application already reads
secrets from a runtime configuration source:

.. code-block:: python

   import os

   from search_smith import BraveSearch

   client = BraveSearch(api_key=os.environ["BRAVE_SEARCH_API_KEY"])

Direct constructor arguments override environment variables. Avoid hard-coding
API keys in Python files, notebooks, shell history, or documentation examples.
The key is only sent in the ``X-Subscription-Token`` request header and is not
included in exceptions, CLI output, or result metadata.

Brave API Mapping
-----------------

The Brave provider uses:

* Endpoint: ``https://api.search.brave.com/res/v1/web/search``
* Header: ``X-Subscription-Token``
* Parameters: ``q``, ``count``, ``offset``, ``result_filter=web``,
  ``text_decorations=false``

Validation follows Brave's documented limits for web search:

* ``count`` must be between 1 and 20.
* ``offset`` must be between 0 and 9.
* ``query`` must not be empty.

Security Considerations
-----------------------

Keep API keys out of source control. Use environment variables locally and
secret managers in CI, containers, and hosted applications. Avoid logging full
request headers because provider authentication data lives there.
