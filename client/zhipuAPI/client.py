from zhipuai import ZhipuAI

from env import get_env_value

Image_client = ZhipuAI(api_key="7d277be9c3fb21b39f1503783badb67a.hHFkZRJaq6v2WVHF")
Image_describe_client=ZhipuAI(api_key="17dd5987b0dd3bd5e949986bd51cad6d.F8utGuSmkBMDZaT1")
Video_client=ZhipuAI(api_key="a542f179df2831b7762f1c1cd251ff8d.NepN5i3RVd1TdkbS")
def generate(text):
    response = Image_client.images.generations(
        model="cogview-3",  # 填写需要调用的模型名称
        prompt=text,
    )

    return response.data[0].url
