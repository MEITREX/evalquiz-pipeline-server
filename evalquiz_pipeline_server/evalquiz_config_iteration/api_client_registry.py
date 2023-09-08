from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.llm_clients.gpt_4_client import (
    GPT4Client,
)


class APIClientRegistry:
    def __init__(self) -> None:
        self.llm_clients = {"gpt-4": GPT4Client(), "gpt-4-32k": GPT4Client("gpt-4-32k")}
