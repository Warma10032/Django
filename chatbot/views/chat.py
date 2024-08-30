import requests
from django.shortcuts import render
from django.http import JsonResponse

def chat_view(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        # 向Flask后端发送请求,在app.py文件中
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

def grodio_chat_view(request):
    return render(request, 'chat.html')

