import openai

from src.models import OpenAIModels

class OpenAILLM:
    """Class for OpenAI LLM."""
    def __init__(self, model_name: str, temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature

    def get_completion(self, messages: list[dict]) -> str:
        """Get prompt completion from OpenAI API."""

        response = openai.ChatCompletion.create(
            model=self.model_name.value,
            messages=messages,
            temperature=self.temperature,
            stream=False,
        )

        return response.choices[0].message["content"]