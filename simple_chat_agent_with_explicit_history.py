from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama.chat_models import ChatOllama

from utils import print_history


LLM = ChatOllama(model="llama3.2")

class State(TypedDict):
    messages: List[HumanMessage]
    output: str

# nodes
def llm_call(state: State):
    # call llm
    response = LLM.invoke(state["messages"])

    return {"output": response.content}    

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
        history.append(AIMessage(response['output']))

        print_history(response["messages"])

        human_input = input("Enter: ")


if __name__ == "__main__":
    main()
