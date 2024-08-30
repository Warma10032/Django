from flask import Flask, request, jsonify
from openai import OpenAI

# 使用flask后端
app = Flask(__name__) 

# 定义了一个Client
class LLMClient(object):
    def __init__(self):
        self.__client = OpenAI(
            api_key = 's',  # get_env_value("LLM_API_KEY"),
            base_url = 'http://localhost:8000/v1/', # get_env_value("LLM_BASE_URL"),
        )
        self.__model_name = 'glm-4' # get_env_value("MODEL_NAME")

    # 装饰器，可以从外部以属性的方式调用
    @property
    def client(self):
        return self.__client
    
    @property
    def model_name(self):
        return self.__model_name
    
    # 主要函数
    def chat_with_ai(self, message):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": message},
            ],
            top_p=0.7,
            temperature=0.95, # 都可以改成从环境变量.env中获取
            max_tokens=1024,
        )
        return response
    
# 触发器
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get("message")
    client = LLMClient()
    response = client.chat_with_ai(message)
    return jsonify({"response": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(debug=True)
