from env import get_env_value
from typing import List,Dict

from openai import OpenAI
from openai.types.chat import ChatCompletion,ChatCompletionChunk
from openai import Stream

from LLMclientbase import LLMclientbase
from overrides import override

# 实例化函数
class LLMclientgeneric(LLMclientbase):
    def __init__(self,*args,**krgs):
        super().__init__

    # 该函数只负责单论对话交流，不包括力是
    @override
    def chat_with_ai(self, prompt: str) -> str | None:
       response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt},
            ],
            top_p=0.7,
            temperature=0.95,
            max_tokens=1024,
       )
       response.choices[0].message.content

    @override
    def chat_with_ai_stream(self, prompt: str,
                            history: List[List[str]] | None = None) -> ChatCompletion | Stream[ChatCompletionChunk]:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.construct_messages(prompt, history if history else []),
            top_p=0.7,
            temperature=0.95,
            max_tokens=1024,
            stream=True,
        )
        return response

    @override
    def construct_message(self, prompt: str, history: List[List[str]] | None = None) -> List[Dict[str,str]]:
        messages = [
        {"role": "system", "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的回答。"}]

        for user_input, ai_response in history:
            messages.append({"role": "user", "content": user_input})
            messages.append(
                {"role": "assistant", "content": ai_response.__repr__()})

        messages.append({"role": "user", "content": prompt})
        return messages
