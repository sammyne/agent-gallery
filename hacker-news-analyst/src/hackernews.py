import json
import logging

import httpx
from langchain.tools import tool

logger = logging.getLogger(__name__)


@tool
def get_top_hackernews_stories(num_stories: int = 10) -> str:
    """Use this function to get top stories from Hacker News.

    Args:
        num_stories (int): Number of stories to return. Defaults to 10.

    Returns:
        str: JSON string of top stories.
    """

    logger.debug(f"Getting top {num_stories} stories from Hacker News")

    # Fetch top story IDs
    response = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    story_ids = response.json()

    # Fetch story details
    stories = []
    for story_id in story_ids[:num_stories]:
        story_response = httpx.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        story = story_response.json()
        story["username"] = story["by"]
        stories.append(story)
    return json.dumps(stories)


@tool
def get_user_details(self, username: str) -> str:
    """Use this function to get the details of a Hacker News user using their username.

    Args:
        username (str): Username of the user to get details for.

    Returns:
        str: JSON string of the user details.
    """

    try:
        logger.debug(f"Getting details for user: {username}")
        user = httpx.get(
            f"https://hacker-news.firebaseio.com/v0/user/{username}.json"
        ).json()
        user_details = {
            "id": user.get("user_id"),
            "karma": user.get("karma"),
            "about": user.get("about"),
            "total_items_submitted": len(user.get("submitted", [])),
        }
        return json.dumps(user_details)
    except Exception as e:
        logger.exception(e)
        return f"Error getting user details: {e}"
