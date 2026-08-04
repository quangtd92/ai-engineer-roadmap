from dataclasses import dataclass


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str

    def __repr__(self) -> str:
        return f"ChatMessage(role={self.role!r}, content={self.content!r})"
