from dataclasses import dataclass


@dataclass
class Message:
    timestamp: str
    username: str
    content: str
