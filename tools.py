from langchain.tools import tool
# Internet se data lene ke liye library
import requests
from bs4 import BeautifulSoup
# “latest AI news” → Tavily fetch karega real results
from tavily import TavilyClient
# System-level operations || API keys secure tarike se lene ke liye
import os
from rich import print
# .env file se secret values load karta hai
from dotenv import load_dotenv
load_dotenv()

tavily =TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic. Return titles , URLs and snippets."""

    results = tavily.search(query=query,max_results=5)
    # CHANGR
    # return results

# print(web_search.invoke("what are the recent news of war?"))
# print(web_search.invoke("what is array "))

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n "
        )
    return "\n----\n".join(out)

# print(web_search.invoke("what are the recent news of war?"))


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clear text content from a given URL for deeper reading."""
    
    try:
        resp = requests.get(url, timeout=8, headers={"user-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    
# print(scrape_url.invoke("https://www.geeksforgeeks.org/"))

# print(scrape_url.invoke("https://sarkariresult.com.cm/"))


