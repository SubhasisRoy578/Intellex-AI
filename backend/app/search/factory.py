from app.config.config import settings
from app.search.provider import BaseSearchProvider, MockSearchProvider, TavilySearchProvider


class SearchProviderFactory:
    """Dynamic resolver factory returning the configured active BaseSearchProvider instance."""

    @staticmethod
    def get_provider() -> BaseSearchProvider:
        provider_name = settings.SEARCH_PROVIDER.lower()

        if provider_name == "tavily" and settings.TAVILY_API_KEY:
            return TavilySearchProvider(api_key=settings.TAVILY_API_KEY)
            
        # Defaults/Fallbacks to extremely safe Mock provider
        return MockSearchProvider()
