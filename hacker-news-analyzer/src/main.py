from datetime import datetime

from dotenv import load_dotenv
from langchain.agents import create_agent

import hackernews
import llm

# Define instructions for the agent
INSTRUCTIONS = """You are an intelligent HackerNews analyst and tech news curator. Your capabilities include:

1. Analyzing HackerNews content:
   - Track trending topics and patterns
   - Analyze user engagement and comments
   - Identify interesting discussions and debates
   - Provide insights about tech trends
   - Compare stories across different time periods

2. When analyzing stories:
   - Look for patterns in user engagement
   - Identify common themes and topics
   - Highlight particularly insightful comments
   - Note any controversial or highly debated points
   - Consider the broader tech industry context

3. When providing summaries:
   - Be engaging and conversational
   - Include relevant context and background
   - Highlight the most interesting aspects
   - Make connections between related stories
   - Suggest why the content matters

Always maintain a helpful and engaging tone while providing valuable insights."""

load_dotenv()

# 初始化 LLM 模型
model = llm.must_new_openai_like()

# Initialize tools
tools = [hackernews.get_top_hackernews_stories, hackernews.get_user_details]

# Create the agent with enhanced capabilities
agent = create_agent(
    model=model,
    name="Tech News Analyst",
    # instructions=[INSTRUCTIONS],
    tools=tools,
    debug=True,
    # model=Nebius(id="Qwen/Qwen3-30B-A3B", api_key=os.getenv("NEBIUS_API_KEY")),
    # markdown=True,
    # memory=True,  # Enable memory for context retention
    system_prompt=INSTRUCTIONS,
)


def main():
    print("🤖 Tech News Analyst is ready!")
    print("\nI can help you with:")
    print("1. Top stories and trends on HackerNews")
    print("2. Detailed analysis of specific topics")
    print("3. User engagement patterns")
    print("4. Tech industry insights")
    print("\nType 'exit' to quit or ask me anything about tech news!")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye! 👋")
            break

        # Add timestamp to the response
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}]")
        query = {"messages": [{"role": "user", "content": user_input}]}
        # agent.print_response(user_input)
        r = agent.invoke(query)
        print(r["messages"][-1].content)


if __name__ == "__main__":
    main()
