from django.shortcuts import render, redirect
from chatbot.models import User
from chatbot.forms import UserForm
from model.RAG.retrieve_model import INSTANCE
import threading
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

from rest_framework import status
from app import start_gradio



# 建议Views分文件存储
# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         if username == 'admin' and password == '123456':  # 这里的用户是固定的，实际上应该加密存储到数据库

#             # # 启动后台线程来为用户加载文件并构建向量库
#             # thread = threading.Thread(target=INSTANCE.build_user_vector_store, args=(username,))
#             # thread.start()

#             return redirect('chat_view')
#         else:
#             return render(request, 'login.html', {'error': 'Invalid credentials'})
#     return render(request, 'login.html')

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         # 假设用户名和密码是固定的，实际情况应该通过数据库验证
#         if username == 'ym' and password == '123456':

#             INSTANCE.set_user_id(username)

#             thread = threading.Thread(target=INSTANCE.build_user_vector_store(), args=(username,))
#             thread.start()

#             # 登录成功后跳转到选择页面
#             return redirect('choice_view')
#         else:
#             # 登录失败，返回登录页面并提示错误
#             return render(request, 'login.html', {'error': 'Invalid credentials'})
    
#     # 显示登录页面
#     return render(request, 'login.html')


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


# 下面的代码目前没用，保留为后续连接数据库进行参考
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})

def user_update(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

def user_delete(request, pk):
    User.objects.get(pk=pk).delete()
    return redirect('user_list')

