from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List


class State(TypedDict):
    name: str 
    age: int
    skills: List[str]
    output: str

def greeting_node(state: State):
    """ Adds greeting message to the final state"""
    state["output"] = f"{state['name']}, welcome to the system! "

    return state

def age_info_node(state: State):
    """ Adds age info message to the final state"""
    state["output"] += f"You are {state['age']} years old! "

    return state

def skills_info(state: State):
    """ Adds skills info into the final state"""
    state["output"] += f"You have skills in: {state['skills'][0]}"
    skill_count = len(state["skills"])

    if skill_count > 1:
        for i in range(1, skill_count):
            if i == skill_count - 1:
                state["output"] += f" and {state['skills'][i]}"
            else:
                state["output"] += f", {state['skills'][i]}"
    
    return state

def main():
    graph = StateGraph(State)
    graph.add_node("first_node", greeting_node)
    graph.add_node("second_node", age_info_node)
    graph.add_node("third_node", skills_info)

    graph.add_edge(START, "first_node")
    graph.add_edge("first_node", "second_node")
    graph.add_edge("second_node", "third_node")
    graph.add_edge("third_node", END)

    workflow = graph.compile()
    result = workflow.invoke({"name": "Annie", "age": 12, "skills": ["Python", "ML", "Langgraph", "English"]})
    print(result["output"])
    

if __name__ == "__main__":
    main()
