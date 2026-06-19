from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents import planner_agent, search_agent, analyst_agent, writer_agent


class ResearchState(TypedDict):
    topic: str
    questions: list[str]
    search_data: list[dict]
    analyses: list[dict]
    report: str


def planner_node(state: ResearchState) -> ResearchState:
    questions = planner_agent(state["topic"])
    state["questions"] = questions
    return state

def search_node(state: ResearchState) -> ResearchState:
    search_data = search_agent(state["questions"])
    state["search_data"] = search_data
    return state

def analyst_node(state: ResearchState) -> ResearchState:
    analyses = analyst_agent(state["search_data"])
    state["analyses"] = analyses
    return state

def writer_node(state: ResearchState) -> ResearchState:
    report = writer_agent(state["topic"], state["analyses"])
    state["report"] = report
    return state


def build_graph():
    workflow = StateGraph(ResearchState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("search", search_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("writer", writer_node)

    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "search")
    workflow.add_edge("search", "analyst")
    workflow.add_edge("analyst", "writer")
    workflow.add_edge("writer", END)

    return workflow.compile()

if __name__ == "__main__":
    graph = build_graph()

    initial_state = {
        "topic": "Impact of AI on entry-level jobs",
        "questions": [],
        "search_data": [],
        "analyses": [],
        "report": ""
    }

    final_state = graph.invoke(initial_state)

    print("\n\n========== FINAL REPORT ==========\n")
    print(final_state["report"])