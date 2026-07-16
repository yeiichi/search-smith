Development
===========

Local Commands
--------------

.. code-block:: bash

   make install
   make format
   make lint
   make test
   make docs
   make build
   make check

``make check`` runs formatting checks, linting, tests, strict documentation
build, and package build.

Releases
--------

Releases are intended to be owned by GitHub Actions and Python Semantic
Release.

1. Merge conventional commits to ``main``.
2. Python Semantic Release computes the version.
3. It updates version metadata and ``CHANGELOG.md``.
4. It creates the release commit, tag, and GitHub release.
5. GitHub Actions builds the package.
6. GitHub Actions publishes to PyPI using trusted publishing/OIDC.

Do not store a long-lived PyPI token in the repository.

Read the Docs
-------------

Documentation publication should be configured in Read the Docs using the
recommended repository integration. GitHub Actions validates
``sphinx-build -W -b html docs/source docs/build/html``, but does not deploy
documentation.

Repository-owner setup:

1. Create or import the ``search-smith`` RTD project.
2. Connect the GitHub repository.
3. Enable builds for ``main``.
4. Confirm ``.readthedocs.yaml`` is detected.
