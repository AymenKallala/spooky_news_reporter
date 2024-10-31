from tavily import TavilyClient
import os
from dotenv import load_dotenv
from swarm.types import Result


load_dotenv()


tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query):
    """
    Perform a web search using the Tavily client and the user query.

    Args:
        query (str): The search query string the user gave.

    Returns:
        list: A list of search results returned by the Tavily client.
    """
    return tavily_client.search(query)


def add_web_search_context(search_results):
    """
    Add web search results to the context dictionary.

    Args:
        search_results (list): The list of web search results to add.

    Modifies:
        context: Adds a 'web_search_results' key with the search results.
    """
    return Result(context_variables = {"web_search_results": search_results})

def add_analysis_context(analysis):
    """
    Add your analysis to the context.

    Args:
        news (list or dict): The news data to add to the context.

    Modifies:
        context: Adds a 'news' key with the provided news data.
    """
    return Result(context_variables ={"analysis": analysis})


def add_story_context(story):
    """
    Add scenario information to the  context dictionary.

    Args:
        scenario (list or dict): The scenario data to add to the context.

    Modifies:
        context: Adds a 'scenarios' key with the provided scenario data.
    """
    return Result(context_variables ={"story": story})