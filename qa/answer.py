from typing import Tuple, List, Any

# , map_question_to_function_args
from qa.function_tool import map_question_to_function
from qa.question_parser import parse_question
from qa.purpose_type import userPurposeType


def get_answer(
    question: str, history: List[List | None] = None, image_url=None
) -> Tuple[Any, userPurposeType]:
    """
    根据问题获取答案或者完成任务
    :param history:
    :param question:
    :return:
    """
    # 判断问题类型，选择不同的函数
    question_type = parse_question(question, image_url)
    print(question_type)

    function = map_question_to_function(question_type)

    args = [question_type, question, history, image_url]
    result = function(*args)

    return result
