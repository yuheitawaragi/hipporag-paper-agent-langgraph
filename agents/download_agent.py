from pathlib import Path

import requests


def download_node(state):

    Path("papers").mkdir(
        exist_ok=True
    )

    papers = []

    for paper in state["papers"]:

        filename = (
            paper["title"]
            .replace("/", "_")
            .replace(":", "_")
            + ".pdf"
        )

        pdf_path = Path("papers") / filename

        if not pdf_path.exists():

            print(
                f"Download : {paper['title']}"
            )

            r = requests.get(
                paper["pdf_url"],
                timeout=60
            )

            with open(
                pdf_path,
                "wb"
            ) as f:

                f.write(r.content)

        paper["pdf_path"] = str(pdf_path)

        papers.append(paper)

    return {
        "papers": papers
    }