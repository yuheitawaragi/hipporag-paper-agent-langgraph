from llm.rag import RAG


from llm.rag import RAG

def answer_node(state):

    rag = RAG()

    print(type(state["retrieved"]))
    print(type(state["retrieved"][0]))
    print(state["retrieved"][0])

    answer = rag.answer(
        question=state["question"],
        contexts=state["retrieved"],
    )

    return {
        "answer": answer
    }