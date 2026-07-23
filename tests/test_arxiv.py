import arxiv

client = arxiv.Client()

search = arxiv.Search(
    query='all:"T cell exhaustion"',
    max_results=5,
    sort_by=arxiv.SortCriterion.Relevance,
)

for paper in client.results(search):
    print("-" * 50)
    print(paper.title)
    print(paper.pdf_url)