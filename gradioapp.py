import gradio as gr
from qa.answer import get_answer
from client.LLMclientgeneric import LLMclientgeneric
from icecream import ic

def grodio_chat_view(message,history):
        ic(message)
        ic(history)
        
        print('zzz')

        response = get_answer(message,history)

        return "hhh"
    
interface = gr.ChatInterface(fn=grodio_chat_view ,
        chatbot=gr.Chatbot(height=400),
        textbox=gr.Textbox(placeholder="请输入你的问题", container=False, scale=7))
interface.launch(server_name="0.0.0.0", server_port=7860)

