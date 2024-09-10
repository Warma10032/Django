from typing import Tuple, List, Any

#, map_question_to_function_args
from qa.function_tool import map_question_to_function
from qa.question_parser import parse_question
from qa.purpose_type import userPurposeType
from qa.question_parser import check_entity
from qa.function_tool import relation_tool

def get_answer(question: str,
               history: List[List | None] = None,image_url=None) -> (
        Tuple[Any, userPurposeType]):
     """
     根据问题获取答案或者完成任务
     :param history:
     :param question:
     :return:
     """
     # 判断问题类型，选择不同的函数
     question_type = parse_question(question,image_url)
     print(question_type)

     kg_info = None
     
     try:
     # 此处在使用知识图谱之前，需先检查问题的实体
          entities = check_entity(question)
          kg_info = relation_tool(entities)
     except:
          pass

     if kg_info is not None:
          question = f'{question}\n从知识图谱中检索到的信息如下{kg_info}\n请你基于知识图谱的信息去回答,并给出知识图谱检索到的信息'

     # entities = check_entity(question)

     function = map_question_to_function(question_type)
     # args_getter = map_question_to_function_args(question_type)
     # args = args_getter([question_type, question, history, entities])

     args = [question_type,question,history,image_url]
     result = function(*args)

     # # 如果上面的代码不行则直接默认问题类型为unknown,就用chat解决
     # if not result:
     #     function = map_question_to_function(QuestionType.UNKNOWN)
     #     args_getter = map_question_to_function_args(QuestionType.UNKNOWN)
     #     args = args_getter([question_type, question, history, entities])
     #     result = function(*args)

     return result
