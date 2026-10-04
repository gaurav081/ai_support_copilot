from app.memory.conversation import ConversationMemory


memory = ConversationMemory()


memory.add_message(
    "user",
    "My order number is 12345."
)

memory.add_message(
    "assistant",
    "I'll help you with order 12345."
)

memory.add_message(
    "user",
    "Where is it?"
)


print("\nConversation:")

for message in memory.get_messages():
    print(
        f"{message['role']}: "
        f"{message['content']}"
    )