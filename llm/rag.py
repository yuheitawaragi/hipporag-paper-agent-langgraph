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

            # LlamaIndex NodeWithScore
            if hasattr(doc, "node"):

                node = doc.node

                title = node.metadata.get(
                    "title",
                    "Unknown"
                )

                authors = node.metadata.get(
                    "authors",
                    []
                )

                published = node.metadata.get(
                    "published",
                    ""
                )

                page = node.metadata.get(
                    "page",
                    ""
                )

                pdf_url = node.metadata.get(
                    "pdf_url",
                    ""
                )

                text = node.text


            # FAISS dict
            else:

                title = doc.get(
                    "title",
                    "Unknown"
                )

                authors = doc.get(
                    "authors",
                    []
                )

                published = doc.get(
                    "published",
                    ""
                )

                page = doc.get(
                    "page",
                    ""
                )

                pdf_url = doc.get(
                    "pdf_url",
                    ""
                )

                text = doc.get(
                    "text",
                    ""
                )


            context += f"""
Title:
{title}

Authors:
{", ".join(authors)}

Published:
{published}

Page:
{page}

PDF:
{pdf_url}

Content:
{text}

------------------------
"""


        prompt = f"""
You are an AI research assistant.

Use ONLY the retrieved paper contents.

If the answer cannot be found in the retrieved papers, reply exactly:

"I don't know."

Instructions:

- Use only the retrieved papers.
- Do not hallucinate.
- Combine information from multiple papers when appropriate.
- After every important statement, cite the paper title in parentheses.
- At the end, provide a References section.
- List each referenced paper only once in the References section.

Retrieved Papers:

{context}


Question:

{question}


Output format:

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