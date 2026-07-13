import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize(title: str, abstract: str):

    prompt = f"""
You are an AI research assistant.

Summarize the following paper.

Title:
{title}

Abstract:
{abstract}

Output in markdown.

## Summary

## Novelty

## Method

## Main Results

## Limitations
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

    return response.choices[0].message.content