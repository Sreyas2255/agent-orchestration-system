from config.llm import llm


def code_agent(task: str, required_inputs: list[str]) -> str:
    """
    Code Specialist Agent.

    Handles coding-related subtasks assigned by the Supervisor.
    """

    inputs = "\n\n".join(required_inputs) if required_inputs else "No previous inputs."

    # Limit input size to avoid Groq TPM limits
    inputs = inputs[:8000]

    prompt = f"""
You are the Code Agent in a multi-agent AI orchestration system.

Coding Task:
{task}

Available Inputs:
{inputs}

Instructions:
- Produce correct and readable code.
- Use the provided information when relevant.
- Keep the solution focused on the assigned task.
- Do not execute the code.
- Return the coding result clearly.
"""

    response = llm.invoke(prompt)

    return response.content