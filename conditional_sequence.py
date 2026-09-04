from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal

class State(TypedDict):
    number1: int
    number2: int
    ops: Literal["+", "-"]
    # decision: str
    output: int


def router_node(state: State):
    """ Just passes the state"""
    
    return state

def router_decision(state: State):
    """ Function that routes which path to choose depending on the input ops"""
    result = "add" if state["ops"] == "+" else "subtract"

    return result

def add_node(state: State):
    """ Function that given two integers sums them"""
    result = state["number1"] + state["number2"]

    return {"output": result}

def subtract_node(state: State):
    """ Function that given two integers subtract second from the first one"""
    result = state["number1"] - state["number2"]

    return {"output": result}


def main():
    graph = StateGraph(State)

    graph.add_node("router_node", router_node)
    graph.add_node("add_node", add_node)
    graph.add_node("subtract_node", subtract_node)

    graph.add_edge(START, "router_node")
    graph.add_conditional_edges("router_node", router_decision, {"add": "add_node", "subtract": "subtract_node"})
    graph.add_edge("add_node", END)
    graph.add_edge("subtract_node", END)

    workflow = graph.compile()

    # visualize
    graph_png = workflow.get_graph().draw_mermaid_png()
    with open("./images/conditional.png", "wb") as f:
        f.write(graph_png)


    result = workflow.invoke({"number1": 2, "number2": 6, "ops": "*"})
    print(result["output"])

if __name__ == "__main__":
    main()
