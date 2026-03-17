from collections import defaultdict
from datetime import datetime, timezone
from secure_api.core.config import get_settings
from secure_api.core.exceptions import RateLimitException

settings = get_settings()


class RateLimiterService:
    """
    Tracks failed login attempts per username using an in-memory store.
    For multi-instance deployments, replace _store with a Redis client.
    """

    def __init__(self) -> None:
        # { username: [(attempt_timestamp), ...] }
        self._store: dict[str, list[datetime]] = defaultdict(list)

    def _purge_old_attempts(self, username: str) -> None:
        """Remove attempts older than the rate limit window."""
        now = datetime.now(timezone.utc)
        window = settings.RATE_LIMIT_WINDOW_SECONDS
        self._store[username] = [
            ts for ts in self._store[username]
            if (now - ts).total_seconds() < window
        ]

    def record_failed_attempt(self, username: str) -> None:
        self._purge_old_attempts(username)
        self._store[username].append(datetime.now(timezone.utc))

    def check_rate_limit(self, username: str) -> None:
        """Raises RateLimitException if the user exceeded allowed attempts."""
        self._purge_old_attempts(username)
        if len(self._store[username]) >= settings.RATE_LIMIT_ATTEMPTS:
            raise RateLimitException()

    def reset(self, username: str) -> None:
        """Clear attempts after a successful login."""
        self._store.pop(username, None)


# Singleton — shared across all requests in the same process
rate_limiter = RateLimiterService()
