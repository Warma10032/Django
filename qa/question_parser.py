from client.clientfactory import Clientfactory

from qa.prompt_templates import get_question_parser_prompt
from qa.purpose_type import purpose_map
from qa.purpose_type import userPurposeType

from icecream import ic


def parse_question(question: str,iamge_url) -> userPurposeType:

    if "文献" in question :
        return purpose_map["基于文件描述"]

    # 在这个函数中我们使用大模型去判断问题类型
    prompt = get_question_parser_prompt(question)
    response = Clientfactory().get_client().chat_with_ai(prompt)
    print(response)
    # 这里暂时还没有实现其他意图的功能,暂时全部设置成其他类型
    #防止问题是空，但是有图片这种情况
    if image_url is not None:
        return purpose_map["图片描述"]
    if response == "图片生成":
        return purpose_map["图片生成"]
    if  response =="视频生成":
        return purpose_map["视频生成"]
    if  response =="PPT生成":
         return purpose_map["PPT生成"]
    if response == "音频生成":
        return purpose_map["音频生成"]
      
    purpose_type = purpose_map["其他"]
    return purpose_type



    
