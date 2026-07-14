import os

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class EmbeddingModel:

    def __init__(
        self,
        model="text-embedding-3-small",
    ):
        self.model = model

    def embed(self, text):

        response = client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding

    def embed_documents(self, chunks):

        embeddings = []

        for chunk in chunks:

            vector = self.embed(
                chunk["text"]
            )

            embeddings.append(vector)

        return embeddings