from graph.workflow import graph


user_input = input("Enter your task: ")

result = graph.invoke({
    "user_input": user_input,
    "research_results": [],
    "data_results": [],
    "code_results": [],
    "writing_results": [],
    "review_result": ""
})


print("\nExecution Plan:")

for i, subtask in enumerate(result["plan"].subtasks, start=1):

    print(f"\nSubtask {i}")
    print(f"Description: {subtask.description}")
    print(f"Specialist: {subtask.assigned_specialist}")
    print(f"Required Inputs: {subtask.required_inputs}")
    print(f"Expected Output: {subtask.expected_output}")
    print(f"Complexity: {subtask.complexity}")


print("\nResearch Results:")

for i, research in enumerate(
    result["research_results"],
    start=1
):
    print(f"\n--- Research Result {i} ---")
    print(research)


print("\nFinal Writing Results:")

for i, writing in enumerate(
    result["writing_results"],
    start=1
):
    print(f"\n--- Final Report {i} ---")
    print(writing)


print("\nReviewer Result:")

print(result["review_result"])