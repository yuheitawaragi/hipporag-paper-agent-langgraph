class ContextBuilder:


    def __init__(
        self,
        max_contexts=20
    ):

        self.max_contexts = max_contexts



    def build(
        self,
        triples
    ):
        """
        Graph Retrieval結果を
        LLM用contextへ変換
        """


        if not triples:
            return ""



        # =====================
        # 1. entity_score順
        # =====================

        triples = sorted(
            triples,
            key=lambda x: x.get(
                "entity_score",
                0
            ),
            reverse=True
        )



        contexts = []

        seen = set()



        # =====================
        # 2. 重複除去
        # =====================

        for triple in triples:


            key = (
                triple["subject"],
                triple["relation"],
                triple["object"]
            )


            if key in seen:
                continue


            seen.add(key)



            contexts.append(
                f"""
Entity:
{triple["subject"]}

Relation:
{triple["relation"]}

Connected Entity:
{triple["object"]}

Entity Importance:
{triple.get("entity_score",0):.4f}
"""
            )


            if len(contexts) >= self.max_contexts:
                break



        return "\n\n".join(
            contexts
        )