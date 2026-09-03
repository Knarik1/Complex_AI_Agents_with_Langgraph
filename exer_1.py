from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class AgentState(TypedDict):
    name: str 
    output: str 

def ai_greeting_node(state: AgentState):
    """ Gets a name and greets the person """

    result = f"Hi {state["name"]}, how are you?"

    # here no difference
    # state["output"] = result
    # return state

    return {"output": result}

def main():
    graph = StateGraph(AgentState)
    graph.add_node("greeting", ai_greeting_node)

    graph.add_edge(START, "greeting")
    graph.add_edge("greeting", END)

    workflow = graph.compile()
    response = workflow.invoke({"name": "Sakura"})
    print(response)


if __name__ == "__main__":
    main()
