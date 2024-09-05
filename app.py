import gradio as gr
from qa.answer import get_answer
from qa.function_tool import process_image_describe_tool

from qa.purpose_type import userPurposeType

from client.LLMclientgeneric import LLMclientgeneric
from icecream import ic

AVATAR = ("resource/user.png", "resource//bot.jpg")


def stream_output(text, chunk_size=5):
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]


# 核心函数


def grodio_chat_view(message, history, image):
    ic(message)
    ic(history)

    ic("是否传入图片：", image)
    if image is not None:
        answer = get_answer(message, history, image_url=image)
    else:
        answer = get_answer(message, history)
    ic("模型回答：", answer)
    
    partial_message = ""
    # 处理文本生成/其他/文档检索
    if answer[1] == userPurposeType.Unknown or answer[1] == userPurposeType.Document:
        # 流式输出
        for chunk in answer[0]:
            partial_message = partial_message + (chunk.choices[0].delta.content or "")
            yield partial_message
    # 处理图片生成
    if answer[1] == userPurposeType.ImageGeneration:
        image_url = answer[0]
        describe = process_image_describe_tool(
            question_type=userPurposeType.ImageDescribe,
            question="描述这个图片",
            history=" ",
            image_url=image_url,
        )
        combined_message = f"""
                        <div>
                        <p>生成的图片：</p>
                        <img src="{image_url}" alt="Generated Image" style="max-width: 100%; height: auto;" />
                        <p>{describe[0] }"</p>
                        </div>
                        """
        yield combined_message
    # 处理图片描述
    if answer[1] == userPurposeType.ImageDescribe:
        output_message = answer[0]
        chunk_size = 1  # 设定每次输出的字符数
        for i in range(0, len(output_message), chunk_size):
            partial_message = output_message[: i + chunk_size]
            yield partial_message
    # 处理视频
    if answer[1] == userPurposeType.Video:
        if answer[0] is not None:
            yield answer[0]
    # 处理
    if answer[1] == userPurposeType.PPT:
        yield answer[0]

    if answer[1] == userPurposeType.Audio:
        yield answer[0]
        
    if answer[1] == userPurposeType.InternetSearch:
        if answer[2]==False:
           partial_message="由于网络问题，访问互联网失败，下面由我根据现有知识给出回答："     
        for chunk in answer[0]:
            partial_message = partial_message + (chunk.choices[0].delta.content or "")
            yield partial_message


# textbox=gr.Textbox(placeholder="请输入你的问题", container=False, scale=7),  # 输入框配置
interface = gr.ChatInterface(
    fn=grodio_chat_view,
    chatbot=gr.Chatbot(height=400, avatar_images=AVATAR, show_copy_button=True),  # 聊天机器人配置
    textbox=gr.Textbox(
        placeholder="请输入你的问题", container=False, scale=7
    ),  # 输入框配置
    additional_inputs=gr.Image(type="filepath", label="上传图像"),
    additional_inputs_accordion_name="你的额外输入",
    title="「赛博华佗」📒",  # 聊天界面的标题
    description="你的健康小助手",  # 聊天界面的描述
    theme="default",  # 主题
    examples=[
        ["您好"],
        ["你会写代码吗"],
        ["给我一个健身计划"],
        ["帮我生成一张老人练太极图片"],
        ["帮我生成一段老人打太极的视频"],
        ["请用粤语朗诵一下 鹅、鹅、鹅，曲项向天歌。白毛浮绿水，红掌拨清波"],
        ["根据文献帮我快速入门git"],
        ["描述这张图片"],
        ["根据搜索，介绍一下东南大学"],
    ],
    cache_examples=False,  # 是否缓存示例输入
    retry_btn=None,  # 重试按钮的配置py
    submit_btn="发送",
    stop_btn="停止",
    undo_btn="删除当前",
    clear_btn="清除所有",
    concurrency_limit=4,  # 并发限制cd
)

interface.launch(share=True)
