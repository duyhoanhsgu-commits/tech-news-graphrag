"""LLM client abstraction."""
from __future__ import annotations

from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    @abstractmethod
    async def complete(self, system: str, user: str) -> str:
        ...


class OpenAILLMClient(BaseLLMClient):
    def __init__(self, model: str = "gpt-4o-mini", api_key: str = "", temperature: float = 0.0, max_tokens: int = 2048) -> None:
        import openai  # type: ignore[import]
        self._client = openai.AsyncOpenAI(api_key=api_key)
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens

    async def complete(self, system: str, user: str) -> str:
        response = await self._client.chat.completions.create(
            model=self._model,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return response.choices[0].message.content or ""
