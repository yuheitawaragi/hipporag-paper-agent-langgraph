import os

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class RAG:

    def __init__(
        self,
        model="gpt-4.1-mini",
    ):
        self.model = model

    def answer(
        self,
        question,
        contexts,
    ):
        context = ""
        for doc in contexts:
            context += f"""
Title:
{doc["title"]}

Authors:
{", ".join(doc["authors"])}

Published:
{doc["published"]}

Page:
{doc["page"]}

PDF:
{doc["pdf_url"]}

Content:
{doc["text"]}

------------------------
"""
            prompt = f"""
You are an AI research assistant.

Use ONLY the retrieved paper contents.

If the answer cannot be found in the retrieved papers, reply exactly:

"I don't know."

Instructions

- Use only the retrieved papers.
- Do not hallucinate.
- Combine information from multiple papers when appropriate.
- After every important statement, cite the paper title in parentheses.
- At the end, provide a References section.
- List each referenced paper only once in the References section, even if it is cited multiple times in the answer.

Retrieved Papers

{context}

Question

{question}

Output format

## Answer

...

## References

1.

Title:
...

Authors:
...

Published:
...

PDF URL:
...

2.

Title:
...

Authors:
...

Published:
...

PDF URL:
...
"""

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content