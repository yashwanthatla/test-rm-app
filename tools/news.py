from langchain_core.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from typing import Dict
from dotenv import load_dotenv

load_dotenv()


class NewsTools:
    @staticmethod
    @tool("search_news")
    def search_news(query: str) -> str:
        """Search for latest news using Serper API."""
        search = GoogleSerperAPIWrapper()
        results = search.run(query)
        return results
