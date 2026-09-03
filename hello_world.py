from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    message: str 

# node
def greeting_node(state: State):
    """ Simple greeting function"""
    result = f"Hi, {state["message"]}, where have you been?"
    # state["message"] = result

    return {"message": result}    
    # return state    


def main():
    workflow = StateGraph(State)
    workflow.add_node("greeting", greeting_node)

    workflow.add_edge(START, "greeting")
    workflow.add_edge("greeting", END)

    app = workflow.compile()

    # visualize
    graph_png = app.get_graph().draw_mermaid_png()
    with open("./images/hello_world.png", "wb") as f:
        f.write(graph_png)

    response = app.invoke({"message": "Sasuke"})   
    print(response["message"]) 


if __name__ == "__main__":
    main()
