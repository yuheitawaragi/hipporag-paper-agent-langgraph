import json

from .models import Triple


class TripleParser:

    def parse(
        self,
        text,
    ):

        data = json.loads(text)

        triples = []

        for row in data:

            triples.append(

                Triple(
                    row["subject"],
                    row["predicate"],
                    row["object"],
                )

            )

        return triples