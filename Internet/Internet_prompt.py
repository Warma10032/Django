from typing import List,Dict
from client.clientfactory import Clientfactory

_GENERATE_Internet_PROMPT_ = "请从最新一轮对话中，替用户提取出属于同一主题的几个可以在搜索引擎上搜索的问题，用分号“；”分隔。（不要有多余的内容）"


def __construct_messages(question: str, history: List[List | None]) -> List[Dict[str, str]]:
    messages = [
        {"role": "system",
         "content": "你现在扮演信息抽取的角色，要求根据用户输入和AI的回答，正确提取出信息，无需包含提示文字"}]

    for user_input, ai_response in history:
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": repr(ai_response)})

    messages.append({"role": "user", "content": question})
    messages.append({"role": "user", "content": _GENERATE_Internet_PROMPT_})

    return messages


def extract_question(question: str,
                 history: List[List | None] | None = None) -> str:
    messages = __construct_messages(question, history or [])
    result = Clientfactory().get_client().chat_using_messages(messages)

    return result
