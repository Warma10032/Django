import gradio as gr
from qa.answer import get_answer
from qa.purpose_type import userPurposeType

from client.LLMclientgeneric import LLMclientgeneric
from icecream import ic

AVATAR = ("resource/user.png",
        "resource//bot.jpg")

# 核心函数
def grodio_chat_view(message,history):
        ic(message)
        ic(history)

        answer = get_answer(message,history)

        partial_message=""
        print(answer)

        # Unknown
        if answer[1] == userPurposeType.Unknown or answer[1] == userPurposeType.Ducument:
            for chunk in answer[0]:
                partial_message = partial_message + (chunk.choices[0].delta.content or "")
                yield partial_message
                
        if answer[1] == userPurposeType.ImageGeneration:
            image_url = answer[0]
            combined_message = f'''
                        <div>
                            <p>生成的图片：</p>
                            <img src="{image_url}" alt="Generated Image" style="max-width: 100%; height: auto;" />
                           
                        </div>
                    '''
            yield combined_message




# textbox=gr.Textbox(placeholder="请输入你的问题", container=False, scale=7),  # 输入框配置
interface = gr.ChatInterface(fn=grodio_chat_view ,
        chatbot=gr.Chatbot(height=400, avatar_images=AVATAR), # 聊天机器人配置
        textbox=gr.Textbox(placeholder="请输入你的问题", container=False, scale=7),  # 输入框配置
        title="「赛博华佗」📒", # 聊天界面的标题
        description="你的健康小助手", # 聊天界面的描述
        theme="default", # 主题
        examples=["您好",  "用python写一个hello world代码","给我一个健身计划","帮我生成一张老人练太极图片","根据文献，解释一下糖尿病"],
        cache_examples=False, # 是否缓存示例输入
        retry_btn=None, # 重试按钮的配置
        submit_btn="发送",
        stop_btn="停止",
        undo_btn="删除当前",
        clear_btn="清除所有",
        concurrency_limit=4, # 并发限制cd

        )
interface.launch()