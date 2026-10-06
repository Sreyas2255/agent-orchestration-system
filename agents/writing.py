from config.llm import llm


def writing_agent(task: str, required_inputs: list[str]) -> str:
    """
    Writing Specialist Agent.

    Uses research, data, and code results to produce
    the requested final output.
    """

    # Limit the amount of information sent to the LLM
    inputs = "\n\n".join(required_inputs)

    # Keep the prompt within Groq's token limit
    inputs = inputs[:6000]

    prompt = f"""
You are the Writing Agent in a multi-agent AI orchestration system.

Your responsibility is to create the final written output
using the information provided by other specialist agents.

Writing Task:
{task}

Information from Other Agents:
{inputs}

Instructions:
- Use the provided information as the primary source.
- Organize the information clearly.
- Do not invent unsupported information.
- Combine relevant findings from the specialist agents.
- Keep the final answer concise and useful.
- Return only the final written output.

Produce the final result.
"""

    response = llm.invoke(prompt)

    return response.content