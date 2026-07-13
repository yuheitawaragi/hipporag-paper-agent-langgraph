from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def planner_node(state):

    prompt = f"""
You are a planner.

Determine which action is needed.

User Query:
{state["question"]}

Available actions:

- search
- answer

Return ONLY one word.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    action = response.choices[0].message.content.strip().lower()

    state["action"] = action

    return state