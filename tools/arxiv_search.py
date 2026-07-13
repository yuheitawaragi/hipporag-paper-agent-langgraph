import arxiv


def search_papers(query: str, max_results: int = 5):
    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        #GraphRAGの最新研究や派生研究を追いたいとき
        #sort_by=arxiv.SortCriterion.SubmittedDate,
        #GraphRAGの最新研究や派生研究を追いたいとき
        sort_by=arxiv.SortCriterion.Relevance,
    )

    papers = []

    for paper in client.results(search):
        papers.append(
            {
                "title": paper.title,
                "authors": [a.name for a in paper.authors],
                "summary": paper.summary,
                "published": paper.published.strftime("%Y-%m-%d"),
                "pdf_url": paper.pdf_url,
                "entry_id": paper.entry_id,
            }
        )

    return papers