from typing import Tuple ,Optional,List
from model.KG.search_model import INSTANCE,_Value

def search(query:str) -> Tuple[int,List[_Value]|None]:
    result = INSTANCE.search(query)
    if result is not None:
        return 0 , result
    else:
        return -1 , None
    
