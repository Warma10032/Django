import gradio as gr
from client.llm_client_generic import LLMClientGeneric


def chat_with_ai(message):
        client = LLMClientGeneric()
        response = client.chat_with_ai(message)
        return response
    
interface = gr.Interface(fn=chat_with_ai, inputs="text", outputs="text")
interface.launch(server_name="0.0.0.0", server_port=7860)

