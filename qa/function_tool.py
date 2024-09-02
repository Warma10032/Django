from typing import Callable,List

from client.clientfactory import Clientfactory
from qa.purpose_type import userPurposeType

# 处理Unkown问题的函数
def process_unknown_tool(question_type,question,history):
    response = Clientfactory().get_client().chat_with_ai_stream(question,history)
    return (response,question_type)

# 处理ImageGeneration问题的函数
def process_images_tool(question_type,question,history):
   print(1)
   print(question_type)
   client=Clientfactory.get_special_client(client_type=question_type)
   response = client.images.generations(
       model="cogview-3",  # 填写需要调用的模型编码
       prompt=question,
   )

   print(response.data[0].url)
   return (response.data[0].url,question_type)

QUESTION_TO_FUNCTION = {
    userPurposeType.Unknown: process_unknown_tool,
    userPurposeType.ImageGeneration: process_images_tool
}


# 根据用户不同的意图选择不同的函数
def map_question_to_function(purpose : userPurposeType) -> Callable:
    if purpose in QUESTION_TO_FUNCTION:
        print (QUESTION_TO_FUNCTION[purpose])
        return QUESTION_TO_FUNCTION[purpose]
    else :
        raise ValueError('没有找到意图对应的函数')
