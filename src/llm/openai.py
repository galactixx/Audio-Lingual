import os
from typing import List

import openai

from src.models.models import (
    OpenAIInstructions,
    OpenAIModels)

if not os.environ.get("OPENAI_API_KEY"):
    
    # The API key is blank or not set
    raise ValueError("OPENAI_API_KEY is not set or is blank")

class OpenAILLM:
    """Simple interface for OpenAI LLM."""
    def __init__(self, model_name: OpenAIModels = OpenAIModels.GPT_3_5_TURBO, temperature: float = 0.65):
        self.model_name = model_name
        self.temperature = temperature

        if model_name.value not in [model.value for model in OpenAIModels]:
            raise ValueError(f'{model_name} is not a valid model name for OpenAI API')
        
    def generate_message_prompt(self, prompt: str, instruction: OpenAIInstructions) -> List[dict]:
        """Generate final message prompt based on prompt parameter input."""
        messages = [{"role": "user", "content": prompt}]
        if instruction is not None:
            messages = [instruction.value] + messages
        return messages

    def get_completion(self, prompt: str, instruction: OpenAIInstructions = OpenAIInstructions.BASIC) -> str:
        """Get prompt completion from OpenAI API."""

        # Generate final message to be parsed by llm
        messages = self.generate_message_prompt(prompt=prompt, instruction=instruction)

        # Chat completion
        response = openai.ChatCompletion.create(
            model=self.model_name.value,
            messages=messages,
            temperature=self.temperature,
            stream=False,
        )

        return response.choices[0].message["content"]