"""Answer generator — sends context + query to the LLM."""
from __future__ import annotations

from graphrag.generation.llm import BaseLLMClient
from graphrag.generation.prompts import ANSWER_SYSTEM, ANSWER_USER


class AnswerGenerator:
    def __init__(self, client: BaseLLMClient) -> None:
        self._client = client

    async def generate(self, query: str, context: str) -> str:
        user = ANSWER_USER.format(context=context, question=query)
        return await self._client.complete(system=ANSWER_SYSTEM, user=user)
