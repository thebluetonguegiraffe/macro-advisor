import os
from langchain_core.tools import tool
from tavily import TavilyClient


@tool(
    description="Searches for recent macroeconomic news using the Tavily API. Use this tool to find"
    " qualitative context, recent events, central bank announcements, or financial market news that"
    " statistical APIs cannot provide. Pass the specific search term in the 'query' argument."
)
def search_macro_news(query: str) -> dict:
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    return client.search(query, max_results=5)
