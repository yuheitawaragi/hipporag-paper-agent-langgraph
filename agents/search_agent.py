from tools.arxiv_search import search_papers

def search_node(state):

    papers = search_papers(state["query"])

    return {
        "papers": papers
    }