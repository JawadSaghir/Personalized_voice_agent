from tavily import TavilyClient
from dotenv import load_dotenv,find_dotenv
import os
_ =load_dotenv(find_dotenv())
API_KEY=os.getenv("GEMINI_API_KEY")
#Getting tavily api key
def websearch_tool(queries:str)->str:
    tavily_api_key=os.getenv("TAVILY_API_KEY")
    tavily_client=TavilyClient(api_key=tavily_api_key)
    response=tavily_client.search(query=queries,
                                search_depth="advanced",
                                include_raw_content="markdown",
                                max_results=1,
                                include_answer="advanced",
                                country="pakistan"
                                )
    # response=tavily_client.crawl(
    #     categories=["Contact"]
    # )
    print(response)
