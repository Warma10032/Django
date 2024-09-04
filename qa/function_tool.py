from typing import Callable,List,Tuple

from client.clientfactory import Clientfactory
from qa.purpose_type import userPurposeType

from rag import rag_chain

from audio.audio_extract import extract_text,extract_language,\
extract_gender,get_tts_model_name

from audio.audio_generate import audio_generate
from kg.Graph import GraphDao

from qa.purpose_type import userPurposeType
from model.KG.search_model import _Value

_dao = GraphDao()

def relation_tool(entities: List[_Value] | None) -> str | None:
    if not entities or len(entities) == 0:
        return "未提供任何实体。"
    
    relationships = set()  # 使用集合来避免重复关系
    relationship_match=[]
    
    # 遍历每个实体并查询与其他实体的关系
    for entity in entities:
        entity_name = entity.name
        
        # 查询每个实体与其他实体的关系
        relationship_match.append(_dao.query_relationship_by_person_name(entity_name)) 
        
    for record in relationship_match:
        # 获取起始节点和结束节点的名称
        start_name = record[0]['r'].start_node['name']
        end_name = record[0]['r'].end_node['name']
        
        # 获取关系类型
        rel = type(record[0]['r']).__name__  # 获取关系的类名，比如 CAUSES
        
        # # 获取关系的备注信息，假设关系中可能有一个 'Notes' 属性
        # notes = getattr(record['r'], 'Notes', '无')
        
        # 构建关系字符串，打印或存储关系信息
        print(f"{start_name} {rel} {end_name}")

            
            # 构建关系字符串并添加到集合，确保不会重复添加
        relationships.add(f"{start_name} {rel} {end_name}")
    
    # 处理实体之间的直接关系，避免重复
    # if len(entities) > 1:
    #     for i in range(len(entities)):
    #         for j in range(i + 1, len(entities)):
    #             entity1_name = entities[i].name
    #             entity2_name = entities[j].name
                
    #             # 查询两个实体之间是否有直接关系
    #             relationship_match_direct = _dao.query_relationship_by_2person_name(entity1_name, entity2_name)
                
    #             if relationship_match_direct:
    #                 start_name = relationship_match_direct[0]['a']['name']
    #                 rel = relationship_match_direct[0]['r']['type']
    #                 end_name = relationship_match_direct[0]['b']['name']
    #                 notes = relationship_match_direct[0]['r'].get('Notes', '无')
                    
    #                 # 添加两个实体之间的直接关系
    #                 relationships.add(f"{start_name} 与 {end_name} 之间的关系是 {rel}，详见备注: {notes}")
    
    # 返回关系集合的内容
    if relationships:
        return "；".join(relationships)
    else:
        return None

# 处理Unkown问题的函数
def process_unknown_tool(question_type : userPurposeType,
             question : str,history:List[List | None]=None):
    response = Clientfactory().get_client().chat_with_ai_stream(question,history)
    return (response,question_type)

# 处理RAG问题
def RAG_tool(question_type : userPurposeType,
             question : str,history:List[List | None]=None):
    # 先利用question去检索得到docs
    response = rag_chain.invoke(question,history)
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

# 处理audio问题的函数
def process_audio_tool(question_type : userPurposeType,
             question : str,history:List[List | None]=None):
    # 先让大语言模型生成需要转换成语音的文字
    text = extract_text(question, history)
    # 判断需要生成哪种语应（川，粤...）
    lang = extract_language(question)
    # 判断需要生成男声还是女声
    gender = extract_gender(question)
    # 上面三步均与大语言模型进行交互
    # 选择用于生成的模型
    model_name = get_tts_model_name(lang=lang, gender=gender)
    audio_file = audio_generate(text, model_name)

    return((audio_file, "语音"),userPurposeType.Audio)

QUESTION_TO_FUNCTION = {
    userPurposeType.Unknown : process_unknown_tool,
    userPurposeType.Ducument : RAG_tool,
    userPurposeType.ImageGeneration: process_images_tool,
    userPurposeType.Audio :process_audio_tool
}


# 根据用户不同的意图选择不同的函数
def map_question_to_function(purpose : userPurposeType) -> Callable:
    if purpose in QUESTION_TO_FUNCTION:
        print (QUESTION_TO_FUNCTION[purpose])
        return QUESTION_TO_FUNCTION[purpose]
    else :
        raise ValueError('没有找到意图对应的函数')
