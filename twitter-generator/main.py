import json
import os

import dotenv
from langchain.agents import create_agent
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from langchain_openai import ChatOpenAI
from langgraph.cache.sqlite import SqliteCache
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


class Page(TypedDict):
    title: str
    content: str


class TweetThread(TypedDict):
    """Tweet Thread"""

    tweet_number: int  # number of tweet
    content: str  # content of tweet


class Tweet(TypedDict):
    """Tweet"""

    thread: list[TweetThread]  # tweet thread details
    total_tweets: int  # total number of tweets in the thread


class State(TypedDict):
    url: str
    page: Page
    tweet: Tweet


def new_openai_like(**kwargs) -> ChatOpenAI:
    return ChatOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ["OPENAI_API_BASE_URL"],
        model=os.environ["OPENAI_MODEL"],
        **kwargs,
    )


def scrape(state: State):
    # ref: https://docs.langchain.com/oss/python/integrations/document_loaders/firecrawl
    loader = FireCrawlLoader(
        api_key=os.environ["FIRECRAWL_API_KEY"], url=state["url"], mode="scrape"
    )
    docs = loader.load()
    return {
        "page": {"title": docs[0].metadata["title"], "content": docs[0].page_content}
    }


def tweet(state: State):
    with open("static/twitter-prompt.txt", "r", encoding="utf-8") as f:
        promptTemplate = f.read()

    page = state["page"]
    prompt = promptTemplate.replace("{{title}}", page["title"]).replace(
        "{{content}}", page["content"]
    )

    # ref: https://docs.langchain.com/oss/python/langchain/structured-output
    agent = create_agent(
        model=new_openai_like(temperature=0.7, max_tokens=2000),
        system_prompt=prompt,
        cache=SqliteCache(path="_cache.sqlite"),
        response_format=Tweet,
    )

    r = agent.invoke({"messages": [("user", prompt)]})
    # print("------------")
    # for v in r["messages"]:
    #     v.pretty_print()

    return {"tweet": r["structured_response"]}


def main():
    dotenv.load_dotenv()

    workflow = StateGraph(State)

    workflow.add_node("scrape", scrape)
    workflow.add_node("tweet", tweet)

    workflow.add_edge(START, "scrape")
    workflow.add_edge("scrape", "tweet")
    workflow.add_edge("tweet", END)

    chain = workflow.compile()

    state = chain.invoke({"url": "https://www.langchain.com/"})

    tweet_json = json.dumps(state["tweet"], indent=2, ensure_ascii=False)
    print(f"\n\ntweet:\n{tweet_json}")


if __name__ == "__main__":
    main()
