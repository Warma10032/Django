import gradio as gr
import base64
from openai import OpenAI
from qa.answer import get_answer
from qa.function_tool import process_image_describe_tool
import speech_recognition as  sr
from qa.purpose_type import userPurposeType

from client.LLMclientgeneric import LLMclientgeneric
from icecream import ic

AVATAR = ("resource/user.png", "resource//bot.jpg")
def stream_output(text, chunk_size=5):
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_encoded

def generate_base64_image_html(image_path):
    base64_encoded = image_to_base64(image_path)
    image_html = f'<img src="data:image/jpeg;base64,{base64_encoded}" alt="Uploaded Image" style="max-width: 200px; height: auto;" />'
    return image_html

def audio_to_text(audio_file_path):
        # 创建识别器对象
        recognizer = sr.Recognizer()
        try:
            # 使用 AudioFile 打开音频文件
            with sr.AudioFile(audio_file_path) as source:
                # 读取音频文件数据
                audio_data = recognizer.record(source)
                # 使用 Google Web Speech API 进行语音识别
                text = recognizer.recognize_google(audio_data, language="zh-CN")  # 使用中文
                return text
        except sr.UnknownValueError:
            return "语音解析出错了"
        except sr.RequestError as e:
            return f" 谷歌演讲API拒绝您的请求   "

def grodio_chat_view(message, history, image,filepath,audio):
     #将语音输入转化为文本
    if audio is not None:
        if len(message)>0:
              message=audio_to_text(audio)+message
        else:
              message =audio_to_text(audio)


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
        if len(message)==0:
            message ="描述这个图片？"
        # 将图片转换为 Base64 格式
        image_html = generate_base64_image_html(image)
        # 合并文本和图片为用户的消息
        user_message = f"您好，您的问题可能是：{message}<br>您上传了：<br>{image_html}<br>下面是我基于现有知识的回答"
        print(type(user_message))
        output_message = answer[0]
        print(type(output_message))
        combined_message = f"{user_message}<br>{output_message}"
     #   chunk_size = 1  # 设定每次输出的字符数
      #  for i in range(0, len( combined_message), chunk_size):
          #  partial_message =  combined_message[: i + chunk_size]
        yield  combined_message
    if answer[1] == userPurposeType.Video:
        if answer[0] is not None:
            yield answer[0]
    # 处理PPT
    if answer[1] == userPurposeType.PPT:
        yield answer[0]
    # 处理音频生成
    if answer[1] == userPurposeType.Audio:
        yield answer[0]
    # 处理联网搜索
    if answer[1] == userPurposeType.InternetSearch:
        if answer[3] == False:
            partial_message = (
                "由于网络问题，访问互联网失败，下面由我根据现有知识给出回答："
            )
        else:
            # 将字典中的内容转换为 Markdown 格式的链接
            links = "\n".join(f"[{title}]({link})" for link, title in answer[2].items())
            links += "\n"
            partial_message = f"参考资料：{links}"
        for chunk in answer[0]:
            partial_message = partial_message + (chunk.choices[0].delta.content or "")
            yield partial_message
  


# textbox=gr.Textbox(placeholder="请输入你的问题", container=False, scale=7),  # 输入框配置
interface = gr.ChatInterface(
    fn=grodio_chat_view,
    chatbot=gr.Chatbot(
        height=400, avatar_images=AVATAR, show_copy_button=True
    ),  # 聊天机器人配置
    textbox=gr.Textbox(
        placeholder="请输入你的问题", container=False, scale=7
    ),  # 输入框配置

    additional_inputs=[
        gr.Image(type="filepath", label="上传图像",every=2),  # 上传图像功能
        gr.File(label="上传知识库", type="filepath"),  # 上传文件功能
        gr.Audio(type="filepath", label="语音输入"),  # 语音输入
    ],
    additional_inputs_accordion_name="你的额外输入",
    title="「赛博华佗」📒",  # 聊天界面的标题
    description="你的健康小助手",  # 聊天界面的描述
    theme="default",  # 主题
    examples=[
         ["您好"],
	     ["我想了解糖尿病相关知识"],
	     ["糖尿病人适合吃的食物有哪些？"],
	     ["糖尿病的常见症状有哪些？"],
         ["帮我生成一份有关糖尿病发病原因丶症状丶治疗药物丶预防措施的PPT"],
         ["请根据我给的就诊信息单，给我一个合理化饮食建议"],
         ["我最近想打太极养生，帮我生成一段老人打太极的视频吧"],
        ["帮我生成一张老人练太极图片"],
        ["帮我生成一段老人打太极的视频"],
        ["请用粤语朗诵一下 鹅、鹅、鹅，曲项向天歌。白毛浮绿水，红掌拨清波"],
        ["根据文献帮我快速入门git"],
        ["搜索一下最新新闻"],
    ],
    cache_examples=False,  # 是否缓存示例输入
    retry_btn=None,  # 重试按钮的配置py
    submit_btn="发送",
    stop_btn="停止",
    undo_btn="删除当前",
    clear_btn="清除所有",
    concurrency_limit=4,  # 并发限制cd
)
interface.launch()
