import json

from .models import Triple


class TripleParser:
    """
    OpenIE JSON parser

    Support:

    1.
    [
      {
        "subject":"",
        "predicate":"",
        "object":""
      }
    ]

    2.
    {
      "triples":[
        {
          "subject":"",
          "predicate":"",
          "object":""
        }
      ]
    }

    """

    def parse(
        self,
        text
    ):

        # =====================================
        # JSON Parse
        # =====================================

        try:

            data = json.loads(
                text
            )

        except Exception:

            print(
                "JSON Parse Error"
            )

            print(text)

            return []


        # =====================================
        # Normalize format
        # =====================================

        if isinstance(
            data,
            dict
        ):

            if "triples" in data:

                data = data["triples"]

            else:

                # unexpected dict
                data = [
                    data
                ]


        # =====================================
        # Build Triple objects
        # =====================================

        triples = []


        for row in data:

            if not isinstance(
                row,
                dict
            ):
                continue


            subject = row.get(
                "subject"
            )

            predicate = row.get(
                "predicate"
            )

            obj = row.get(
                "object"
            )


            if (
                subject is None
                or predicate is None
                or obj is None
            ):
                continue


            triples.append(

                Triple(
                    subject,
                    predicate,
                    obj
                )

            )


        return triples