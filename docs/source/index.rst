search-smith
============

``search-smith`` provides a compact provider-neutral interface for web search.
The first release implements Brave Web Search and exposes both a high-level
helper and an explicit provider client.

Background
----------

Programmatic web search is often a small but important part of evidence
collection, fact-checking, and retrieval workflows. As older APIs such as
Google's Custom Search JSON API become harder to rely on for new projects,
applications need a thin layer that can normalize results without tying the
rest of the codebase to one provider.

Search APIs also differ in meaningful ways: some operate their own web index,
some expose search-engine result pages through a commercial API, and some are
optimized for AI retrieval rather than broad public web search. ``search-smith``
starts with Brave Search, which provides public web results from Brave's
independent search index, while keeping the provider boundary small enough for
future alternatives.

Install
-------

.. code-block:: bash

   uv add search-smith

For local development:

.. code-block:: bash

   uv sync --all-groups

Configure Brave
---------------

Create a Brave Search API key from Brave's API dashboard, then set:

.. code-block:: bash

   export BRAVE_SEARCH_API_KEY="your-api-key"

The package also accepts explicit key injection when the value comes from your
application's runtime configuration:

.. code-block:: python

   import os

   from search_smith import BraveSearch

   client = BraveSearch(api_key=os.environ["BRAVE_SEARCH_API_KEY"])

Do not commit API keys. Prefer environment variables or your deployment
platform's secret store.

Contents
--------

.. toctree::
   :maxdepth: 2

   usage
   configuration
   api
   development
