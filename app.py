from graph import graph
import os
#from evaluate_ragas import evaluate_rag

query = input("Search keyword: ")

question = input("Question: ")

state = {
    "query": query,
    "question": question,
}

result = graph.invoke(state)

#score = evaluate_rag(
    #query=question,
    #retrieved_contexts=result["retrieved"],
    #answer=result["answer"],
    #openai_api_key=os.environ["OPENAI_API_KEY"],
#)

print("\n==========================")
print("RAGAS")
print("==========================")

#print(score)

print("\n==========================")
print("Summary")
print("==========================")

print(result["summary"])

print("\n==========================")
print("Answer")
print("==========================")

print(result["answer"])

print(type(result["retrieved"]))
print(result["retrieved"])