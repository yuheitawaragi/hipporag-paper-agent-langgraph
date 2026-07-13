from datasets import Dataset

from ragas import evaluate
from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)

from langchain_openai import ChatOpenAI


def evaluate_rag(
    query: str,
    retrieved_contexts: list,
    answer: str,
    openai_api_key: str,
):
    """
    RAGAS evaluation

    Parameters
    ----------
    query : str
        User question

    retrieved_contexts : list
        Contexts actually retrieved by the Retriever

    answer : str
        LLM generated answer

    openai_api_key : str
        OpenAI API Key
    """

    # LangChain Document の場合は page_content を取り出す
    contexts = []

    for doc in retrieved_contexts:

        if hasattr(doc, "page_content"):
            contexts.append(doc.page_content)

        else:
            contexts.append(str(doc))

    dataset = Dataset.from_dict(
    {
        "question": [query],
        "contexts": [contexts],
        "answer": [answer],
    }
)

    evaluator_llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0,
        api_key=openai_api_key,
    )

    result = evaluate(
        dataset,
        metrics=[
            Faithfulness(),
            AnswerRelevancy(),
            #ContextPrecision(),
            #ContextRecall(),
        ],
        llm=evaluator_llm,
    )

    return result