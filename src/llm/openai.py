import os
import openai
from typing import Optional, List

from src.models.models import (
    OpenAIInstructions,
    OpenAIModels)

if not os.environ.get("OPENAI_API_KEY"):
    
    # The API key is blank or not set
    raise ValueError("OPENAI_API_KEY is not set or is blank")

def generate_message_prompt(prompt: str, instruction: Optional[OpenAIInstructions] = None) -> List[dict]:
    messages = [{"role": "user", "content": prompt}]
    if instruction is not None:
        messages = [instruction.value] + messages
    return messages

class OpenAILLM:
    """Class for OpenAI LLM."""
    def __init__(self, model_name: OpenAIModels = OpenAIModels.GPT_3_5_TURBO, temperature: float = 0.65):
        self.model_name = model_name
        self.temperature = temperature

        if model_name.value not in [model.value for model in OpenAIModels]:
            raise ValueError(f'{model_name} is not a valid model name for OpenAI API')

    def get_completion(self, messages: list[dict]) -> str:
        """Get prompt completion from OpenAI API."""

        response = openai.ChatCompletion.create(
            model=self.model_name.value,
            messages=messages,
            temperature=self.temperature,
            stream=False,
        )

        return response.choices[0].message["content"]