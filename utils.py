from langchain_core.messages import HumanMessage, AIMessage

def print_history(messages):
    print("\n" + "=" * 60)
    print("                    CONVERSATION")
    print("=" * 60)

    for i, message in enumerate(messages, 1):
        if isinstance(message, HumanMessage):
            print(f"\n👤 You [{i}]")
            print("-" * 40)
            print(message.content)

        elif isinstance(message, AIMessage):
            print(f"\n🤖 AI [{i}]")
            print("-" * 40)
            print(message.content)

    print("\n" + "=" * 60)