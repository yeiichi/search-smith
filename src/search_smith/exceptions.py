"""Package-specific exceptions."""


class SearchSmithError(Exception):
    """Base exception for search-smith failures."""


class ConfigurationError(SearchSmithError):
    """Raised when required configuration is missing or invalid."""


class AuthenticationError(SearchSmithError):
    """Raised when a provider rejects authentication credentials."""


class RateLimitError(SearchSmithError):
    """Raised when a provider rate limit is reached."""


class ProviderError(SearchSmithError):
    """Raised when a provider or network request fails."""
