from django.shortcuts import render, redirect
from .models import User
from .forms import UserForm

# 建议Views分文件存储
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == 'admin' and password == '123456':  # 这里的用户是固定的，实际上应该加密存储到数据库
            return redirect('user_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


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

