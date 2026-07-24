from pathlib import Path

from tools.pdf_downloader import download_pdf


def download_node(state):
    """
    arXivから取得したPDFをダウンロードする
    """

    pdf_dir = Path("papers")
    pdf_dir.mkdir(exist_ok=True)

    papers = []

    for paper in state["papers"]:

        pdf_path = download_pdf(
            paper["pdf_url"],
            pdf_dir
        )

        paper["pdf_path"] = str(pdf_path)

        papers.append(paper)

    return {
        "papers": papers
    }