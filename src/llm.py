from enum import Enum
from typing import Dict, List
from openai import OpenAI, Stream
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from pydantic import BaseModel


class LLM:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model_name: str,
        max_tokens: int = 100,
        top_k: int = 50,
        top_p: float = 0.9,
        temperature: float = 0.2,
        interrupt_repeat: bool = False,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.top_k = top_k
        self.top_p = top_p
        self.temperature = temperature
        self.interrupt_repeat = interrupt_repeat

        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def chat(
        self, messages: List[Dict], stream=False, tools: Dict = None, json_format=False
    ):
        response: ChatCompletion | Stream[ChatCompletionChunk] = (
            self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                stream=stream,
                tools=tools if tools else None,
                response_format={"type": "json_object"} if json_format else None,
            )
        )
        return response
