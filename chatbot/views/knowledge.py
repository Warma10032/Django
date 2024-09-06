from django.shortcuts import render
from django.contrib.auth.decorators import login_required  
from model.RAG.retrieve_model import INSTANCE
import threading


def upload_and_build( uploaded_file):
    # 先上传文件
    INSTANCE.upload_user_file(uploaded_file)
    # 然后更新知识库
    INSTANCE.build_user_vector_store()

# 构建知识库页面视图
#@login_required  # 确保只有登录用户才能访问此页面
def build_knowledge_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        # 上传文件并构建知识库
        if action == 'upload':
            uploaded_file = request.FILES.get('knowledge_file')
            if uploaded_file:
                thread = threading.Thread(target=upload_and_build, args=(uploaded_file,))
                thread.start()
                uploaded_files = INSTANCE.list_uploaded_files()
                return render(request, 'build_knowledge.html', {'success': '知识库文件上传成功！', 'uploaded_files': uploaded_files})
            else:
                return render(request, 'build_knowledge.html', {'error': '请上传文件。'})

        # 展示文件
        elif action == 'list_files':
            uploaded_files =INSTANCE.list_uploaded_files()
            return render(request, 'build_knowledge.html', {'uploaded_files': uploaded_files})

        # 删除文件
        elif action == 'delete_file':
            filename = request.POST.get('filename')
            if filename:
                INSTANCE.delete_uploaded_file(filename=filename)
                uploaded_files = INSTANCE.list_uploaded_files()  # 重新获取文件列表
                return render(request, 'build_knowledge.html', {'success': f'文件 {filename} 删除成功！', 'uploaded_files': uploaded_files})
            else:
                uploaded_files = INSTANCE.list_uploaded_files()
                return render(request, 'build_knowledge.html', {'error': '请指定要删除的文件。', 'uploaded_files': uploaded_files})

    # 如果是GET请求，显示上传页面并展示已上传的文件
    uploaded_files = INSTANCE.list_uploaded_files()
    return render(request, 'build_knowledge.html', {'uploaded_files': uploaded_files})
