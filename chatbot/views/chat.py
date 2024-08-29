import requests
from django.shortcuts import render,redirect
from django.http import JsonResponse
import gradio as gr
from icecream import ic

def chat_main(message,history):
    ic(history)
    ic(message)
    answers = get_answer(message, history)
    
    if request.method == "POST":
        user_message = request.POST.get("message")
        # 向Flask后端发送请求
        response = requests.post(
            "http://127.0.0.1:5000/chat",
            json={"message": user_message}
        )
        # 处理Flask后端的响应
        if response.status_code == 200:
            ai_response = response.json().get("response")
            return JsonResponse({"response": ai_response})
        else:
            return JsonResponse({"error": "Failed to get response from AI"}, status=500)
    return render(request, "chat.html")


# def chat_view(request):
#     iface = gr.Interface(
#         fn=gradio_chat_interface,
#         inputs="text",
#         outputs="text",
#         title="Chat with AI",
#         description="Enter a message and receive a response from the AI."
#     )

#     # 使用 `launch` 方法生成 FastAPI 应用
#     app, _, _ = iface.launch(server_name="localhost", server_port=9000, share=False, inline=False, inbrowser=False, debug=True, prevent_thread_lock=True)
    
#     return redirect("http://localhost:9000")


def run_webui():
    chat_app = gr.ChatInterface(
        chat_main,
        chatbot=gr.Chatbot(height=400, avatar_images=__AVATAR),
        textbox=gr.Textbox(placeholder="请输入你的问题", container=False, scale=7),
        title="「遇见李白」📒",
        description="你可以问关于李白的一切",
        theme="default",
        examples=["您好", "李白与高力士的关系是什么", "杜甫是谁", "李白会写代码吗", "请生成李白在江边喝酒的图片",
                  "你认为杜甫最好的一首诗是哪一首？", "请将这首诗转成语音", "请将这首诗转成语音,语种设置为陕西话","根据参考文献回答，李白在哪里出生",
                  "请根据以下白话文来搜索相应的古文，白话文的内容为，守孝期在古代是多长",
                  "请根据以下古文来搜索相应的古文，古文的内容为，床前明月光","请总结上述内容，然后生成ppt"],
        cache_examples=False,
        retry_btn=None,
        submit_btn="发送",
        stop_btn="停止",
        undo_btn="删除当前",
        clear_btn="清除所有",
        concurrency_limit=4,
    ) 

    chat_app.launch(server_name="localhost"
                    , server_port=8080
                    , share=False
                    , max_threads=10)
    
    return redirect("http://localhost:8080")

