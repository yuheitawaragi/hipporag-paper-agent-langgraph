from pathlib import Path

from llm.summarizer import summarize


def summary_node(state):

    report = ""

    Path("output").mkdir(exist_ok=True)

    for paper in state["papers"]:

        result = summarize(
            paper["title"],
            paper["summary"],
        )

        report += f"# {paper['title']}\n\n"

        report += result

        report += "\n\n"

    with open(
        "output/report.md",
        "w",
        encoding="utf-8",
    ) as f:

        f.write(report)

    state["summary"] = report

    return {
    "summary": report
}