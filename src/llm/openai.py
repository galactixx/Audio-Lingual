import os
from typing import List

import openai

from src.llm.base import BaseLLM
from src.models.models import (
    OpenAIInstructions,
    OpenAIModels)

if not os.environ.get("OPENAI_API_KEY"):
    
    # The API key is blank or not set
    raise ValueError("OPENAI_API_KEY is not set or is blank")

class OpenAILLM(BaseLLM):
    """Simple interface for OpenAI LLM."""
    def __init__(self,
                 model_name: OpenAIModels = OpenAIModels.GPT_3_5_TURBO,
                 instruction: OpenAIInstructions = OpenAIInstructions.BASIC,
                 temperature: float = 0.65):
        self.model_name = model_name
        self.instruction = instruction
        self.temperature = temperature

        if model_name.value not in [model.value for model in OpenAIModels]:
            raise ValueError(f'{model_name} is not a valid model name for OpenAI API')
        
    def generate_message_prompt(self, prompt: str) -> List[dict]:
        """Generate final message prompt based on prompt parameter input."""
        messages = [{"role": "user", "content": prompt}]
        if self.instruction is not None:
            messages = [self.instruction.value] + messages
        return messages

    def get_completion(self, prompt: str) -> str:
        """Get prompt completion from OpenAI API."""

        # Generate final message to be parsed by llm
        messages = self.generate_message_prompt(prompt=prompt, instruction=self.instruction)

        # Chat completion
        response = openai.ChatCompletion.create(
            model=self.model_name.value,
            messages=messages,
            temperature=self.temperature,
            stream=False,
        )

        return response.choices[0].message["content"]