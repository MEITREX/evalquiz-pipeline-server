import os
import openai
from datetime import timedelta
from cs import ratelimit
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.llm_clients.llm_client import (
    LLMClient,
)

openai.api_type = "azure"
openai.api_version = "2023-08-01-preview"
openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base = "https://evalquizuk.openai.azure.com/"
if openai.api_key is None:
    raise ValueError("OpenAI key is not set, therefore no requests can be made.")


class GPT4Client(LLMClient):
    def __init__(self, variant: str = "gpt-4"):
        self.variant = variant

    @ratelimit.ratelimited(max_count=1, interval=timedelta(seconds=5), block=True)
    def request_result_text(self, messages: list[dict[str, str]]) -> str:
        completion = openai.ChatCompletion.create(
            deployment_id="EvalQuiz-GPT4", model=self.variant, messages=messages
        )
        return completion["choices"][0]["message"]["content"]
