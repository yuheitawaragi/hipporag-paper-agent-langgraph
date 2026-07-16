import os

from openai import OpenAI

from .prompt import OPENIE_PROMPT

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class OpenIEExtractor:

    def extract(
        self,
        text,
    ):

        prompt = OPENIE_PROMPT.format(
            text=text
        )

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )

        return response.choices[0].message.content