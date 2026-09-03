from typing import TypedDict, List, Literal
from langgraph.graph import StateGraph, START, END
from functools import reduce



class AgentState(TypedDict):
    name: str 
    values: List[int]
    operation: Literal["+", "*"]
    output: str 

def perform_operation_node(state: AgentState):
    """ Gets name, values and an operation and based on operation sign performs the operation"""
    result = ""

    if state["operation"] == "+":
        result = reduce(lambda a, b: a+b, state["values"])
    elif state["operation"] == "*":
        result = reduce(lambda a, b: a*b, state["values"])

    state["output"] = f"Hi {state['name']}, your answer is: {result}"    

    return state
    

def main():
    graph = StateGraph(AgentState)
    graph.add_node("perform_operation", perform_operation_node)

    graph.add_edge(START, "perform_operation")
    graph.add_edge("perform_operation", END)

    workflow = graph.compile()
    response = workflow.invoke({"name": "Mary", "values": [3, 4], "operation": "*"})
    print(response["output"])


if __name__ == "__main__":
    main()
