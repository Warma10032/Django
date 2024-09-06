from typing import Tuple ,Optional,List,Dict
from model.KG.search_model import INSTANCE,_Value

def search(query:str) -> Tuple[int,List[Dict]|None]:
    result = INSTANCE.search(query)
    if result is not None:
        return 0 , result
    else:
        return -1 , None
    
