from typing import Tuple, List, Any

#, map_question_to_function_args
from qa.function_tool import map_question_to_function
from qa.question_parser import parse_question
from qa.purpose_type import userPurposeType


def get_answer(question: str,
               history: List[List | None] = None) -> (
        Tuple[Any, userPurposeType]):
    """
    根据问题获取答案或者完成任务
    :param history:
    :param question:
    :return:
    """
    # 判断问题类型，选择不同的函数
    question_type = parse_question(question)
    print(question_type)

    

    # entities = check_entity(question)

    function = map_question_to_function(question_type)
    # args_getter = map_question_to_function_args(question_type)
    # args = args_getter([question_type, question, history, entities])

    args = [question_type,question,history]

    result = function(*args)

    # # 如果上面的代码不行则直接默认问题类型为unknown,就用chat解决
    # if not result:
    #     function = map_question_to_function(QuestionType.UNKNOWN)
    #     args_getter = map_question_to_function_args(QuestionType.UNKNOWN)
    #     args = args_getter([question_type, question, history, entities])
    #     result = function(*args)

    return result
