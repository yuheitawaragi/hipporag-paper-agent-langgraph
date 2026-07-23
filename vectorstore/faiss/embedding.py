import os

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class EmbeddingModel:

    def __init__(
        self,
        model="text-embedding-3-small",
        batch_size=100,
    ):
        self.model = model
        self.batch_size = batch_size

    def embed(self, text):
        """
        単一テキストのEmbedding
        """

        response = client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding

    def embed_documents(self, chunks):
        """
        チャンクをバッチ単位でEmbeddingする
        """

        texts = [chunk["text"] for chunk in chunks]

        embeddings = []

        total = len(texts)

        print(f"Embedding {total} chunks...")

        for start in range(0, total, self.batch_size):

            end = min(start + self.batch_size, total)

            batch = texts[start:end]

            print(
                f"Embedding batch "
                f"{start}-{end-1} / {total}"
            )

            response = client.embeddings.create(
                model=self.model,
                input=batch,
            )

            embeddings.extend(
                [
                    item.embedding
                    for item in response.data
                ]
            )

        print("Embedding complete.")

        return embeddings