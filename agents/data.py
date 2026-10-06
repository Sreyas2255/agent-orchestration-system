from config.llm import llm


def data_agent(task: str, required_inputs: list[str]) -> str:
    """
    Data Specialist Agent.

    Handles data analysis and data-related subtasks
    assigned by the Supervisor.
    """

    inputs = "\n\n".join(required_inputs) if required_inputs else "No previous inputs."

    prompt = f"""
You are the Data Agent in a multi-agent AI orchestration system.

Your responsibility is to handle data analysis tasks assigned
by the Supervisor.

Data Analysis Task:
{task}

Available Inputs:
{inputs}

Instructions:
- Analyze the provided information carefully.
- Identify important patterns, trends, or relationships.
- Perform calculations when appropriate.
- Clearly explain the findings.
- Do not invent data that was not provided.
- Keep the analysis focused on the assigned task.
- Return the findings in a format that other agents can easily use.

Return the data analysis results clearly.
"""

    response = llm.invoke(prompt)

    return response.content