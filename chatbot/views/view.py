from django.shortcuts import render, redirect
from chatbot.models import User
from chatbot.forms import UserForm
from model.RAG.retrieve_model import INSTANCE
import threading

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

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # 假设用户名和密码是固定的，实际情况应该通过数据库验证
        if username == 'ym' and password == '123456':

            INSTANCE.set_user_id(username)

            thread = threading.Thread(target=INSTANCE.build_user_vector_store(), args=(username,))
            thread.start()

            # 登录成功后跳转到选择页面
            return redirect('choice_view')
        else:
            # 登录失败，返回登录页面并提示错误
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    # 显示登录页面
    return render(request, 'login.html')

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

