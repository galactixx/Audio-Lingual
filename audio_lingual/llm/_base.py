from typing import List

from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """Base interface for LLM."""
    @abstractmethod
    def generate_message_prompt(self, prompt: str) -> List[dict]:
        pass

    @abstractmethod
    def get_completion(self, prompt: str) -> str:
        pass