import gradio as gr
from qa.answer import get_answer
from qa.purpose_type import userPurposeType

from client.LLMclientgeneric import LLMclientgeneric
from icecream import ic

# 核心函数
def grodio_chat_view(message,history):
        ic(message)
        ic(history)
        
        print('zzz')

        answer = get_answer(message,history)

        partial_message=""

        # Unkno
        if answer[1] == userPurposeType.Unknown:
            for chunk in answer[0]:
                partial_message = partial_message + (chunk.choices[0].delta.content or "")
                yield partial_message

    
interface = gr.ChatInterface(fn=grodio_chat_view ,
        chatbot=gr.Chatbot(height=400),
        textbox=gr.Textbox(placeholder="请输入你的问题", container=False, scale=7))
interface.launch(server_name="0.0.0.0", server_port=7860)

