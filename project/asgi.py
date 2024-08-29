"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
import gradio as gr
from fastapi.middleware.wsgi import WSGIMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# 获取 Django ASGI 应用
django_asgi_app = get_asgi_application()

# 定义 Gradio 应用接口
def gradio_interface(user_message):
    return "Hello " + user_message

# 启动 Gradio 应用，防止启动独立服务器
gradio_app, _, _ = gr.Interface(
    fn=gradio_interface, 
    inputs="text", 
    outputs="text"
).launch(
    share=False, 
    inline=False, 
    prevent_thread_lock=True
)

# 创建 FastAPI 应用
fastapi_app = FastAPI()

# 将 Django ASGI 应用挂载到 FastAPI
fastapi_app.mount("/", WSGIMiddleware(django_asgi_app))

# 将 Gradio 应用挂载到 "/gradio" 路径
fastapi_app.mount("/gradio", gradio_app)

# 设置 ASGI 应用为 FastAPI 应用
application = fastapi_app
