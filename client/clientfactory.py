from client.ourAPI.client import OurAPI
from client.zhipuAPI.client import Image_client, Image_descride_client
from client.zhipuAPI.client import Video_client
from env import get_env_value
from qa.purpose_type import userPurposeType


class Clientfactory:
    map_client_dict = {
        get_env_value("LLM_BASE_URL")
    }
      
    def __init__(self) :
        self._client_url = get_env_value("LLM_BASE_URL")
        self._api_key = get_env_value("LLM_API_KEY")
        #self._sanity_check()
       
    
    # 选择 , 这里我们暂时只用自己的API，不需要选择client
    # def _sanity_check():
        
    #     pass
 
    # 注意python面向对象里面的函数会自动传入一个self类,所以参数里面必须加上self,否则会报错
    def get_client(self):
          return OurAPI()


    @staticmethod
    def get_special_client(client_type:str):
        print(userPurposeType.ImageGeneration)
        if client_type == userPurposeType.ImageGeneration:
            print(3)
            return Image_client
        if client_type == userPurposeType.Unknown:
            return OurAPI()
        if client_type == userPurposeType.ImageDescribe:
            return Image_descride_client
        if client_type == userPurposeType.Audio:
            print(8)
            return Video_client

        print(5)
        #默认情况下使用文本生成模型
        return OurAPI()