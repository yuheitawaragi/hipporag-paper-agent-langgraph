from openai import OpenAI


class EntityEmbedder:

    def __init__(
        self,
        model="text-embedding-3-small",
        batch_size=500
    ):

        self.client = OpenAI()

        self.model = model

        self.batch_size = batch_size


    def embed(
        self,
        texts
    ):

        """
        Batch embedding for OpenAI Embedding API.

        Args:
            texts:
                List[str]

        Returns:
            List[List[float]]
        """


        # ==================================
        # Clean entities
        # ==================================

        cleaned_texts = []


        for text in texts:

            # None除外
            if text is None:
                continue


            # 文字列以外除外
            if not isinstance(text, str):
                continue


            # 空文字・空白除外
            text = text.strip()

            if text == "":
                continue


            cleaned_texts.append(text)



        # ==================================
        # Empty input check
        # ==================================

        if len(cleaned_texts) == 0:

            print(
                "No valid entities for embedding."
            )

            return []



        all_embeddings = []


        total = len(cleaned_texts)


        # ==================================
        # Batch Processing
        # ==================================

        for start in range(
            0,
            total,
            self.batch_size
        ):

            end = min(
                start + self.batch_size,
                total
            )


            batch = cleaned_texts[start:end]


            print(
                f"Embedding entities "
                f"{start}-{end} / {total}"
            )


            response = (
                self.client.embeddings.create(

                    model=self.model,

                    input=batch

                )
            )


            embeddings = [

                item.embedding

                for item in response.data

            ]


            all_embeddings.extend(
                embeddings
            )


        return all_embeddings