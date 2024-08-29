from env import get_env_value

class Clientfactory:
    map_client_dict = {
        get_env_value("LLM_BASE_URL")
    }
      
    def __init__(self) -> None:
        self._client_url = get_env_value("LLM_BASE_URL")
        self._api_key = get_env_value("LLM_API_KEY")
        self._sanity_check()
        pass
    
    # 选择
    def _sanity_check():
        
        pass
 
    def get_client():
        return OurAPI
        pass