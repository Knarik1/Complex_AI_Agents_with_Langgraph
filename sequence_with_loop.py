from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
from random import randint


class State(TypedDict):
    lower_bound: int
    higher_bound: int
    max_guess: int
    attempts: int
    guesses: List[int]
    final: int

# nodes    
def setup_fn(state: State):
    state["lower_bound"] = 1
    state["higher_bound"] = 20
    state["max_guess"] = 7
    state["attempts"] = 0
    state["guesses"] = []

    return state 

def guess_fn(state: State):
    guessed = randint(-100, 100)

    state["guesses"].append(guessed)
    state["attempts"] += 1

    return state

def checker_decision_maker(state: State):
    # returns the edges
    if state["guesses"][-1] in range(state["lower_bound"], state["higher_bound"] + 1):
        return "Finish"
    elif state["attempts"] < state["max_guess"]:
        return "Loop"
    else:
        print("No attempts left")
        return "Fail"

def main():
    chain = StateGraph(State)

    chain.add_node("setup_node", setup_fn) 
    chain.add_node("guess_node", guess_fn)

    chain.add_edge(START, "setup_node")
    chain.add_edge("setup_node", "guess_node")
    chain.add_conditional_edges("guess_node", checker_decision_maker, {"Finish": END, "Loop": "guess_node", "Fail": END})

    workflow = chain.compile()

    # visualize
    graph_png = workflow.get_graph().draw_mermaid_png()
    with open("./images/loop.png", "wb") as f:
        f.write(graph_png)

    result = workflow.invoke({})
    print(result)    


if __name__ == "__main__":
    main()
