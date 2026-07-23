from graph import graph
import os

from evaluate_ragas import evaluate_rag


print("=" * 50)
print("Paper Search AI")
print("=" * 50)

mode = input(
    "Mode (rag / hipporag / hybrid) [hybrid]: "
).strip().lower()

if mode == "":
    mode = "hybrid"

query = input("Search keyword: ")

question = input("Question: ")

state = {
    "query": query,
    "question": question,
    "mode": mode,
}

print("Start graph.invoke")
result = graph.invoke(state)
print("End graph.invoke")

# ==========================
# RAGAS (optional)
# ==========================

print("Start RAGAS")
score = evaluate_rag(
     query=question,
     retrieved_contexts=result["retrieved"],
     answer=result["answer"],
     openai_api_key=os.environ["OPENAI_API_KEY"],
 )
print("End RAGAS")

print("\n==========================")
print(f"Mode : {mode}")
print("==========================")


print("\n==========================")
print("Summary")
print("==========================")

print(result["summary"])


print("\n==========================")
print("Answer")
print("==========================")

print(result["answer"])


print("\n==========================")
print("Retrieved Contexts")
print("==========================")

print(type(result["retrieved"]))

print(len(result["retrieved"]))

if len(result["retrieved"]) > 0:
    print(result["retrieved"][0])


print("\n==========================")
print("RAGAS")
print("==========================")

print(score)