class EntityLinker:


    def __init__(
        self,
        store,
        embedder,
        threshold=0.85
    ):

        self.store = store
        self.embedder = embedder
        self.threshold = threshold



    def link_entity(
        self,
        mention
    ):

        embedding = self.embedder.embed(
            [mention]
        )[0]


        results = self.store.search(
            embedding,
            k=1
        )


        if not results:
            return mention


        candidate = results[0]


        if candidate["score"] >= self.threshold:

            return candidate["entity"]


        return mention



    def normalize(
        self,
        triple
    ):

        triple.subject = self.link_entity(
            triple.subject
        )


        triple.object = self.link_entity(
            triple.object
        )


        return triple