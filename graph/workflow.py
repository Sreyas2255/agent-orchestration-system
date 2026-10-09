from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents.supervisor import supervisor_agent
from agents.research import research_agent
from agents.writing import writing_agent
from agents.data import data_agent
from agents.code import code_agent
from agents.reviewer import reviewer_agent

from schemas.task import ExecutionPlan


class AgentState(TypedDict):
    user_input: str
    plan: ExecutionPlan

    research_results: list[str]
    data_results: list[str]
    code_results: list[str]
    writing_results: list[str]

    review_result: str

    needs_research: bool
    needs_data: bool
    needs_code: bool
    needs_writing: bool


def supervisor_node(state: AgentState):
    """
    Supervisor Agent.

    Creates an execution plan and determines which
    specialist agents are required.
    """

    plan = supervisor_agent(state["user_input"])

    specialists = [
        subtask.assigned_specialist.lower()
        for subtask in plan.subtasks
    ]

    needs_research = "research agent" in specialists
    needs_data = "data agent" in specialists
    needs_code = "code agent" in specialists
    needs_writing = "writing agent" in specialists

    return {
        "plan": plan,
        "needs_research": needs_research,
        "needs_data": needs_data,
        "needs_code": needs_code,
        "needs_writing": needs_writing
    }
def route_after_supervisor(state: AgentState):
    if state["needs_research"]:
        return "research"

    if state["needs_data"]:
        return "data"

    if state["needs_code"]:
        return "code"

    return "writing"


def route_after_research(state: AgentState):
    if state["needs_data"]:
        return "data"

    if state["needs_code"]:
        return "code"

    return "writing"


def route_after_data(state: AgentState):
    if state["needs_code"]:
        return "code"

    return "writing"


def route_after_code(state: AgentState):
    return "writing"    

def research_node(state: AgentState):
    """
    Execute all subtasks assigned to the Research Agent.
    """

    results = []

    for subtask in state["plan"].subtasks:

        if subtask.assigned_specialist.lower() == "research agent":

            result = research_agent(
                subtask.description,
                subtask.required_inputs
            )

            results.append(result)

    return {
        "research_results": results
    }


def data_node(state: AgentState):
    """
    Execute all subtasks assigned to the Data Agent.
    """

    results = []

    research_results = state.get("research_results", [])

    for subtask in state["plan"].subtasks:

        if subtask.assigned_specialist.lower() == "data agent":

            inputs = []

            inputs.extend(subtask.required_inputs)
            inputs.extend(research_results)

            result = data_agent(
                subtask.description,
                inputs
            )

            results.append(result)

    return {
        "data_results": results
    }


def code_node(state: AgentState):
    """
    Execute all subtasks assigned to the Code Agent.
    """

    results = []

    research_results = state.get("research_results", [])
    data_results = state.get("data_results", [])

    for subtask in state["plan"].subtasks:

        if subtask.assigned_specialist.lower() == "code agent":

            inputs = []

            inputs.extend(subtask.required_inputs)
            inputs.extend(research_results)
            inputs.extend(data_results)

            result = code_agent(
                subtask.description,
                inputs
            )

            results.append(result)

    return {
        "code_results": results
    }


def collect_results(state: AgentState):
    """
    Collect specialist results before sending them
    to the Writing Agent.
    """

    return {
        "research_results": state.get("research_results", []),
        "data_results": state.get("data_results", []),
        "code_results": state.get("code_results", [])
    }


def writing_node(state: AgentState):
    """
    Writing Agent creates the final output.
    """

    results = []

    research_results = state.get("research_results", [])
    data_results = state.get("data_results", [])
    code_results = state.get("code_results", [])

    inputs = []

    inputs.extend(research_results)
    inputs.extend(data_results)
    inputs.extend(code_results)

    for subtask in state["plan"].subtasks:

        if subtask.assigned_specialist.lower() == "writing agent":

            result = writing_agent(
                subtask.description,
                inputs
            )

            results.append(result)

    return {
        "writing_results": results
    }


def reviewer_node(state: AgentState):
    """
    Reviewer Agent evaluates the final output.
    """

    execution_plan = str(state["plan"])

    final_output = "\n\n".join(
        state.get("writing_results", [])
    )

    review = reviewer_agent(
        original_task=state["user_input"],
        execution_plan=execution_plan,
        final_output=final_output
    )

    return {
        "review_result": review
    }


# ============================================================
# CREATE LANGGRAPH
# ============================================================

builder = StateGraph(AgentState)


# ============================================================
# ADD NODES
# ============================================================

builder.add_node("supervisor", supervisor_node)
builder.add_node("research", research_node)
builder.add_node("data", data_node)
builder.add_node("code", code_node)
builder.add_node("collect_results", collect_results)
builder.add_node("writing", writing_node)
builder.add_node("reviewer", reviewer_node)


# ============================================================
# DEFINE WORKFLOW
# ============================================================

builder.add_edge(START, "supervisor")


builder.add_conditional_edges(
    "supervisor",
    route_after_supervisor,
    {
        "research": "research",
        "data": "data",
        "code": "code",
        "writing": "writing"
    }
)


builder.add_conditional_edges(
    "research",
    route_after_research,
    {
        "data": "data",
        "code": "code",
        "writing": "writing"
    }
)


builder.add_conditional_edges(
    "data",
    route_after_data,
    {
        "code": "code",
        "writing": "writing"
    }
)


builder.add_conditional_edges(
    "code",
    route_after_code,
    {
        "writing": "writing"
    }
)


builder.add_edge("writing", "reviewer")

builder.add_edge("reviewer", END)


# ============================================================
# COMPILE GRAPH
# ============================================================

graph = builder.compile()