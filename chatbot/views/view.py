from django.shortcuts import render, redirect
from model.RAG.retrieve_model import INSTANCE
import threading
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from app import start_gradio

from chatbot.encrypt import md5
from chatbot import forms
from chatbot import models

# 建议Views分文件存储


# 登录函数
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # 使用 authenticate 来验证用户名和密码
    user = authenticate(username=username, password=password)
    print('zzzz')
    
    if user is not None:
        # 假设用户名和密码匹配成功
        INSTANCE.set_user_id(username)

        # 启动构建用户向量存储的线程
        thread = threading.Thread(target=INSTANCE.build_user_vector_store(), args=(username,))
        thread.start()

        thread_2 = threading.Thread(target=start_gradio)
        thread_2.daemon = True
        thread_2.start()
        # 返回成功响应
        return Response({'message': '登录成功'}, status=200)
    else:
        # 登录失败，返回错误信息
        return Response({'message': '用户名或密码错误'}, status=401)

# 注册函数
@csrf_exempt
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # 检查用户名是否已经存在
    if User.objects.filter(username=username).exists():
        return JsonResponse({'message': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)

    # 检查邮箱是否已经存在
    if User.objects.filter(email=email).exists():
        return JsonResponse({'message': '邮箱已存在'}, status=status.HTTP_400_BAD_REQUEST)

    # 创建用户并将密码加密存储到数据库
    try:
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # 使用 make_password() 进行加密
        )
        return JsonResponse({'message': '注册成功'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({'message': f'注册失败: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 选择页面视图
def choice_view(request):
    if request.method == 'POST':
        # 根据用户的选择跳转到不同的页面
        if 'dialogue' in request.POST:
            return redirect('chat_view')  # 重定向到对话页面
        elif 'build_knowledge' in request.POST:
            return redirect('build_knowledge_view')  # 重定向到构建知识库页面

    # 显示选择页面
    return render(request, 'choice.html')

