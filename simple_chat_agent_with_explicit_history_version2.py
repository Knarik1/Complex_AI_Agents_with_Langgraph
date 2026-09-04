from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama.chat_models import ChatOllama

from utils import print_history


LLM = ChatOllama(model="llama3.2")

class State(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

# nodes
def llm_call(state: State):
    """ Function to call LLM and put the returned response back to messages"""
    # call llm
    response = LLM.invoke(state["messages"])
    state["messages"].append(AIMessage(response.content))

    return state    

def main():
    chain = StateGraph(State)
    chain.add_node("llm_call_node", llm_call)

    chain.add_edge(START, "llm_call_node")
    chain.add_edge("llm_call_node", END)

    workflow = chain.compile()

    history = []
    human_input = input("Enter: ")

    while human_input != "exit":
        history.append(HumanMessage(human_input))
        response = workflow.invoke({"messages": history})

        # save to history
        history = response["messages"]
        print_history(response["messages"])

        human_input = input("Enter: ")


if __name__ == "__main__":
    main()
