from typing import List, Dict

from client.clientfactory import Clientfactory

from qa.prompt_templates import get_question_parser_prompt
from qa.purpose_type import purpose_map
from qa.purpose_type import userPurposeType

from icecream import ic


def parse_question(question: str, image_url) -> userPurposeType:

    if "根据知识库" in question:
        return purpose_map["基于知识库"]
    
    if "根据知识图谱" in question:
        return purpose_map["基于知识图谱"]

    if "搜索" in question:
        return purpose_map["网络搜索"]

    if image_url is not None:
        return purpose_map["图片描述"]

    # 在这个函数中我们使用大模型去判断问题类型
    prompt = get_question_parser_prompt(question)
    response = Clientfactory().get_client().chat_with_ai(prompt)
    ic(response)

    if response == "图片生成" and len(question) > 0:
        return purpose_map["图片生成"]
    if response == "视频生成" and len(question) > 0:
        return purpose_map["视频生成"]
    if response == "PPT生成" and len(question) > 0:
        return purpose_map["PPT生成"]
    if response == "Word生成" and len(question) > 0:
        return purpose_map["Word生成"]
    if response == "音频生成" and len(question) > 0:
        return purpose_map["音频生成"]
    if response == "文本生成":
        return purpose_map["其他"]
    return purpose_map["其他"]



