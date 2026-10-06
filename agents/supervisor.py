from config.llm import llm
from schemas.task import ExecutionPlan


def supervisor_agent(user_input: str) -> ExecutionPlan:
    """
    Supervisor Agent.

    Analyzes the user's request and creates a structured
    execution plan.
    """

    prompt = f"""
You are the Supervisor Agent in a multi-agent AI orchestration system.

Your job is to analyze the user's request and break it into
logical, ordered subtasks.

For every subtask, identify:

- What needs to be done
- Which specialist should handle it
- What inputs are required
- What output is expected
- The complexity: Low, Medium, or High

Available specialists:

- Research Agent
- Data Agent
- Writing Agent
- Code Agent

Do not execute the task yourself.
Only create the execution plan.

User request:
{user_input}
"""

    structured_llm = llm.with_structured_output(ExecutionPlan)

    plan = structured_llm.invoke(prompt)

    return plan