import json

# 假设 raw_json 是一个包含JSON内容的字符串
raw_json= '''
{"title": "糖尿病", "pages": [{"title": "糖尿病概述", "content": [{"title": "糖尿病的定义", "description": "糖尿病是一种慢性代谢性疾病，主要特征是血糖水平持续升高。"}, {"title": "糖尿病的类型", "description": "1型糖尿病：自身免疫性疾病，胰岛素分泌不足。2型糖尿病：胰岛素抵抗或分泌不足。"}]}, {"title": "糖尿病的症状", "content": [{"title": "典型症状", "description": "多尿、多饮、多食、体重减轻。"}, {"title": "非典型症状", "description": "视力模糊、皮肤干燥、疲劳、感染等。"}]}, {"title": "糖尿病的诊断", "content": [{"title": "诊断方法", "description": "血糖测定、糖耐量测试、胰岛素测定等。"}, {"title": "诊断标准", "description": "空腹血糖≥7.0mmol/L或餐后2小时血糖≥11.1mmol/L。。"}]}]}
'''
print(raw_json )
index_of_last_dot = raw_json.rfind('。')
print(index_of_last_dot)
# 输出字符串末尾的五个字符
print(raw_json[-2:])

# 使用 json.loads 解析 JSON 字符串
try:
    data = json.loads(raw_json)
    print("解析成功:", data)
except json.JSONDecodeError as e:
    print("解析失败:", e)


tese=None
print(tese+"你好")