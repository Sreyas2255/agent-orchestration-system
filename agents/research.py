from config.llm import llm


def research_agent(task: str, required_inputs: list[str]) -> str:
    """
    Research Specialist Agent.

    Receives a research subtask from the Supervisor
    and produces the requested research output.
    """

    inputs = "\n".join(required_inputs) if required_inputs else "No previous inputs."

    prompt = f"""
You are the Research Agent in a multi-agent AI orchestration system.

Your responsibility is to complete research-related subtasks
assigned by the Supervisor.

Research Task:
{task}

Required Inputs:
{inputs}

Instructions:
- Focus only on the assigned research task.
- Use the provided inputs when available.
- Provide clear and factual information.
- Organize the result so another agent can easily use it.
- Do not attempt to complete tasks assigned to other specialists.
- Do not create the final report unless specifically asked.

Return the research findings clearly.
"""

    response = llm.invoke(prompt)

    return response.content

if __name__ == "__main__":
    result = research_agent(
        "Explain the fundamentals of Retrieval-Augmented Generation (RAG), including its main components and workflow.",
        []
    )

    print("\nResearch Agent Output:")
    print(result)