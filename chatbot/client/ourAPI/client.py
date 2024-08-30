from openai import OpenAI
from LLMclientgeneric import LLMclientgeneric

class OurAPI(LLMclientgeneric):
    def __init__(self,*args,**krgs):
        super().__init__(*args,**krgs)