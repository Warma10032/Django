# views.py
import requests
import gradio as gr
from django.shortcuts import render
from django.shortcuts import redirect
from fastapi import FastAPI
from django.http import HttpResponse
from django.core.handlers.asgi import ASGIHandler

def gradio_chat_interface(user_message):
    try:
        response = requests.post(
            "http://127.0.0.1:5000/chat",
            json={"message": user_message}
        )
        if response.status_code == 200:
            ai_response = response.json().get("response")
            return ai_response
        else:
            return "Failed to get response from AI"
    except Exception as e:
        return str(e)

def chat_view(request):
    iface = gr.Interface(
        fn=gradio_chat_interface,
        inputs="text",
        outputs="text",
        title="Chat with AI",
        description="Enter a message and receive a response from the AI."
    )

    # 使用 `launch` 方法生成 FastAPI 应用
    app, _, _ = iface.launch(server_name="localhost", server_port=7965, share=False, inline=False, inbrowser=False, debug=True, prevent_thread_lock=True)
    
    return redirect("http://localhost:7865")
