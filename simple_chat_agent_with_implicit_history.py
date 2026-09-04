from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Any, Annotated
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_ollama.chat_models import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
import operator

from utils import print_history


LLM = ChatOllama(model="llama3.2")

class State(TypedDict):
    # need this Annotated with the add operator to reduce the messages
    messages: Annotated[List[BaseMessage], operator.add]
    output: str

# nodes
def llm_call(state: State):
    """ Function to call LLM and put the returned response back to messages"""
    # call llm
    response = LLM.invoke(state["messages"])
    state["messages"].append(AIMessage(response.content))

    # don't return the whole messages, just the last response, it will then be concatenated to others
    return {"output": response.content, "messages": [response]}    

def main():
    chain = StateGraph(State)
    chain.add_node("llm_call_node", llm_call)

    chain.add_edge(START, "llm_call_node")
    chain.add_edge("llm_call_node", END)

    # to save the thread conversations, but this is in-memory
    memory = MemorySaver()
    workflow = chain.compile(checkpointer=memory)

    # start the conversation
    human_input = input("Enter: ")

    while human_input != "exit":
        # for memory you should also give the config
        response = workflow.invoke({"messages": [HumanMessage(human_input)]}, config={"configurable": {"thread_id": "conv-1"}})
        print_history(response["messages"])
        human_input = input("Enter: ")

if __name__ == "__main__":
    main()
