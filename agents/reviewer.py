from config.llm import llm


def reviewer_agent(
    original_task: str,
    execution_plan: str,
    final_output: str
) -> str:
    """
    Reviewer Agent.

    Reviews the final output produced by the specialist agents
    and determines whether it satisfies the original task.
    """

    prompt = f"""
You are the Reviewer Agent in a multi-agent AI orchestration system.

Your responsibility is to review the final output produced by
the other agents.

Original User Task:
{original_task}

Execution Plan:
{execution_plan}

Final Output:
{final_output}

Review the output using these criteria:

1. Accuracy
   - Does the output contain reasonable and consistent information?

2. Completeness
   - Does it address the important parts of the user's task?

3. Relevance
   - Does it stay focused on the requested task?

4. Structure
   - Is the output clear and well organized?

5. Requirements
   - Does it follow the expected output described in the execution plan?

Give a review with:

- Score: a number from 1 to 10
- Status: PASS or REJECT
- Strengths: important things done well
- Issues: problems that should be fixed
- Recommendation: what should happen next

Do not rewrite the final answer.
Only review it.
"""

    response = llm.invoke(prompt)

    return response.content