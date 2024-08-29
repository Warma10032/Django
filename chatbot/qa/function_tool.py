# 这个文件存向大模型服务器发送各种功能请求的函数

from client.clientfactory import Clientfactory

# 在这个函数中去实现文生文对话
def chat_with_ai(question:str):
    response = Clientfactory().get_client().chat.completions.create(
            # model=self.model_name,
            messages=[
                {"role": "user", "content": question},
            ],
            top_p=0.7,
            temperature=0.95, # 都可以改成从环境变量.env中获取
            max_tokens=1024,
        )