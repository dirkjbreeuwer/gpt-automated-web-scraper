"""gpt_interaction.py: A module to interact with GPT models using the OpenAI API."""
import os
from typing import Optional

import openai

from dotenv import load_dotenv

load_dotenv()


class GPTInteraction:
    """A class to interact with GPT models using the OpenAI API."""

    _supported_chat_models = [
        "gpt-4",
        "gpt-4-0314",
        "gpt-4-32k",
        "gpt-4-32k-0314",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-0301",
    ]
    _supported_completion_models = ["text-davinci-003"]

    def __init__(
        self,
        api_token: Optional[str] = None,
        model: str = "gpt-4",
        temperature: float = 1,
        max_tokens: int = 4096,
        top_p: float = 1,
    ):
        """
        Initialize the GPTInteraction class with the required parameters.

        :param api_token: OpenAI API key, defaults to None
        :param model: GPT model to use, defaults to "gpt-4"
        :param temperature: Sampling temperature for the model, defaults to 1
        :param max_tokens: Maximum number of tokens for the model to generate, defaults to 4096
        :param top_p: Nucleus sampling parameter, defaults to 1
        """
        self.api_token = api_token or os.getenv("OPENAI_API_KEY")
        if self.api_token is None:
            raise ValueError("OpenAI API key is required")
        openai.api_key = self.api_token

        if model not in self._supported_chat_models + self._supported_completion_models:
            raise ValueError("Unsupported model")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p

    def call(self, prompt: str) -> str:
        """
        Call the GPT model with the given prompt and return the response.

        :param prompt: The input prompt to send to the model
        :return: The generated text from the GPT model
        """
        if self.model in self._supported_completion_models:
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
            )
        elif self.model in self._supported_chat_models:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "system", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
            )
        else:
            raise ValueError("Unsupported model")

        return response["choices"][0]["message"]["content"]
