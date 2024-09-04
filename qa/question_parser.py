from typing import List

from client.clientfactory import Clientfactory

from qa.prompt_templates import get_question_parser_prompt
from qa.purpose_type import purpose_map
from qa.purpose_type import userPurposeType

from model.KG.search_service import search
from model.KG.search_model import _Value

from icecream import ic

def parse_question(question: str) -> userPurposeType:

    if "文献" in question :
        return purpose_map["基于文件描述"]

    # 在这个函数中我们使用大模型去判断问题类型
    prompt = get_question_parser_prompt(question)
    response = Clientfactory().get_client().chat_with_ai(prompt)
    print(response)
    # 这里暂时还没有实现其他意图的功能,暂时全部设置成其他类型
    if response == "其他":
        return purpose_map["其他"]
    if response == "图片生成":
        return purpose_map["图片生成"]
    if response == "音频生成":
        return purpose_map["音频生成"]
  #默认情况
    purpose_type = purpose_map["其他"]
    return purpose_type



def check_entity(question:str) -> List[_Value]|None:
    code,result = search(question)
    if code == 0:
        return result
    else:
        return None