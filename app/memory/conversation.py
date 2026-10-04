from dataclasses import dataclass, field


@dataclass
class Message:
    role: str
    content: str


@dataclass
class ConversationMemory:
    messages: list[Message] = field(
        default_factory=list
    )

    def add_message(
        self,
        role: str,
        content: str
    ) -> None:

        self.messages.append(
            Message(
                role=role,
                content=content
            )
        )

    def get_messages(self) -> list[dict]:

        return [
            {
                "role": message.role,
                "content": message.content
            }
            for message in self.messages
        ]

    def clear(self) -> None:

        self.messages.clear()