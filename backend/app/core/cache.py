import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple


class BaseCacheBackend(ABC):
    """Abstract interface defining standard contracts for pluggable cache engines."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Gets value from cache."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Saves a value in cache with a TTL limit."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Deletes a key from cache."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Flushes the entire cache space."""
        pass


class InMemoryCacheBackend(BaseCacheBackend):
    """Production-grade in-memory thread-safe dictionary cache with expiration (TTL) checks."""

    def __init__(self) -> None:
        # Maps key -> (value, expire_at_timestamp)
        self._cache: Dict[str, Tuple[Any, float]] = {}

    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
            
        value, expire_at = self._cache[key]
        if time.time() > expire_at:
            # Lazy cleanup on access
            self.delete(key)
            return None
            
        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        duration = ttl if ttl is not None else 300
        expire_at = time.time() + duration
        self._cache[key] = (value, expire_at)
        
        # Periodic inline garbage collection of expired entries to prevent memory bloating
        self._evict_expired_entries()

    def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        self._cache.clear()

    def _evict_expired_entries(self) -> None:
        """Removes expired entries from cache to optimize memory footprint."""
        now = time.time()
        expired_keys = [k for k, (_, exp) in self._cache.items() if now > exp]
        for k in expired_keys:
            del self._cache[k]


# Global cache instance
cache_service = InMemoryCacheBackend()
