import os
import json

from openai import OpenAI

from .prompt import OPENIE_PROMPT


client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


class OpenIEExtractor:


    def __init__(
        self,
        model="gpt-4.1-mini"
    ):

        self.model = model



    def extract(
        self,
        text,
    ):

        # ==================================
        # Prompt
        # ==================================

        prompt = OPENIE_PROMPT.format(
            text=text
        )


        try:

            response = client.chat.completions.create(

                model=self.model,

                messages=[

                    {
                        "role": "system",
                        "content":
                        """
You are an information extraction system.
Extract knowledge graph triples.
Return ONLY valid JSON.
No markdown.
No explanation.
"""
                    },

                    {
                        "role": "user",
                        "content": prompt,
                    }

                ],

                temperature=0,


                # JSON保証
                response_format={
                    "type": "json_object"
                }

            )


        except Exception as e:


            print(
                "[OpenIEExtractor] API Error"
            )

            print(e)


            return "[]"



        # ==================================
        # Response
        # ==================================

        content = (
            response
            .choices[0]
            .message
            .content
        )


        if not content:

            return "[]"



        # ==================================
        # Validate JSON
        # ==================================

        try:

            json.loads(
                content
            )


        except json.JSONDecodeError:


            print(
                "[OpenIEExtractor] Invalid JSON"
            )

            print(
                content[:500]
            )


            return "[]"



        return content