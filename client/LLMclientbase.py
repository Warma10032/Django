from env import get_env_value
from abc import abstractmethod

from openai import OpenAI
from openai import Stream
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from typing import List, Dict

# 抽象类，用于构造client
class LLMclientbase(object):
    def __init__(self):
        self.__client = OpenAI(
            api_key=get_env_value("LLM_API_KEY"),
            base_url=get_env_value("LLM_BASE_URL"),
        )
        self.__model_name = get_env_value("MODEL_NAME")

    @property
    def client(self):
        return self.__client
    
    @property
    def model_name(self):
        return self.__model_name

    # 一下全都是抽象函数
    @abstractmethod
    def chat_with_ai(self, prompt: str) -> str | None:
        raise NotImplementedError()

    @abstractmethod
    def chat_with_ai_stream(self, prompt: str,
                            history: List[List[str]] | None = None) -> ChatCompletion | Stream[ChatCompletionChunk]:
        raise NotImplementedError()

    @abstractmethod
    def construct_message(self, prompt: str, history: List[List[str]] | None = None) -> List[Dict[str,str]] | str | None:
        raise NotImplementedError()

    @abstractmethod
    def chat_using_messages(self, messages: List[Dict]) -> str | None:
        raise NotImplementedError()
