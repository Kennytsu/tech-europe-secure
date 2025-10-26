# Hey Telo - AI Engineering Challenge

## Important

Please do **NOT** share your solution with anyone except the Hey Telo (Admyral Technologies GmbH) team.
Submit your solution only in the GitHub repository you were invited to.

We will provide you with API keys to the services necessary to build a solution to this challenge (OpenAI).

## Background

You are an AI Engineer working at the startup McTelo that is building voice agents for Drive Thrus.

## Task

A McDonald's restaurant is piloting the voice agent that you and the team built using LiveKit.
The restaurant manager is happy with the voice agent but in order to actually use it in production, they need to be able to see the incoming orders.
Your task is to build a pipeline that not only extracts the orders from the voice agent's conversation but also gives the restaurant staff insights
on the quality of the conversations with the customers. Additionally, build a dashboard (preferably Next.js) that shows the restaurant staff the orders
and quality metrics you are capturing.

Some data points that are interesting to capture:

- Order
- Order success (Did the voice agent successfully process the order?)
- Summary of the conversation
- Duration of the conversation
- Transcript of the conversation
- Customer sentiment

Are there any other data points worth capturing that can help us improve the voice agent and give the restaurant staff insights on the quality of the conversations?

## Time

You should spend roughly 4 hours on this task.

## Bonus Points

- Think about observability, scalability and reliability (especially in terms of failures) of the pipeline. How would your architecture look like if the voice agent would be deployed in thousands of McDonald's Drive Thrus in the world?
- Let the agent ask the customer for feedback at the end of the conversation.
- Let the agent handle McDonald's coupons and promotions.
- Any ideas on improving the voice agent's performance and reliability?

## Setup

### Prerequisites

- Python 3.12
- `uv` (https://docs.astral.sh/uv/)

### Configuration

Store the necessary API keys in a `.env` file. You can use the `.env.example` file as a template.

```
OPENAI_API_KEY=...
```

### Usage

Note: the agent is running in console mode for now for ease of use.

```bash
# Start the voice agent on the console
cd agent
uv run python -m drive_thru.agent console
```

In order to shut down the agent, you can press `Ctrl+C` in the terminal (**Hint:** only press `Ctrl+C` once to let the agent gracefully shut down).

## Resources

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [DeepWiki livekit/agents](https://deepwiki.com/livekit/agents)
