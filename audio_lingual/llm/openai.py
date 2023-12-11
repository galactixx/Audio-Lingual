import os
from typing import List

from openai import OpenAI

from audio_lingual.llm._base import BaseLLM
from audio_lingual.models.models import (
    OpenAIInstructions,
    OpenAIModels
)

class OpenAILLM(BaseLLM):
    """
    Simple interface for OpenAI LLM.
    """
    def __init__(
        self,
        model_name: OpenAIModels = OpenAIModels.GPT_3_5_TURBO,
        instruction: OpenAIInstructions = OpenAIInstructions.BASIC,
        temperature: float = 0.70):
        self._model_name = model_name
        self._instruction = instruction
        self._temperature = temperature

        self._api_key = os.environ.get("OPENAI_API_KEY")

        # The API key is blank or not set
        if not self._api_key:
            raise ValueError("OPENAI_API_KEY is not set or is blank")

        if model_name.value not in [model.value for model in OpenAIModels]:
            raise ValueError(f'{model_name} is not a valid model name for OpenAI API')
        
        self._client = OpenAI(api_key=self._api_key)

    def generate_message_prompt(self, prompt: str) -> List[dict]:
        """
        Generate final message prompt based on prompt parameter input.
        """

        messages = [{"role": "user", "content": prompt}]
        if self._instruction is not None:
            messages = [self._instruction.value] + messages
        return messages

    def get_completion(self, prompt: str) -> str:
        """
        Get prompt completion from OpenAI API.
        """

        # Generate final message to be parsed by llm
        messages = self.generate_message_prompt(prompt=prompt)

        # Chat completion
        response = self._client.chat.completions.create(
            model=self._model_name.value,
            messages=messages,
            temperature=self._temperature,
            stream=False,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content