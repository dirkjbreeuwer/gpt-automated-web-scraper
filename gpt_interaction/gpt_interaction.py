import os
from typing import Optional

import openai

from dotenv import load_dotenv

load_dotenv()


class GPTInteraction:
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
        if self.model in self._supported_completion_models:
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p
            )
        elif self.model in self._supported_chat_models:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "system", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p
            )
        else:
            raise ValueError("Unsupported model")

        return response["choices"][0]["message"]["content"]
