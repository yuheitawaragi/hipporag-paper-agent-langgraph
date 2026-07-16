class ContextBuilder:


    def build(
        self,
        triples
    ):
        """
        triplesをLLM入力形式へ変換
        """


        contexts = []


        for triple in triples:

            contexts.append(
                f"""
{triple["subject"]}
 -- {triple["relation"]} -->
{triple["object"]}
"""
            )


        return "\n".join(
            contexts
        )