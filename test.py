import json

# 假设 raw_json 是一个包含JSON内容的字符串
raw_json= '''
{"title": "糖尿病知识", "pages": [{"title": "糖尿病概述", "content": [{"title": "糖尿病的定义", "description": "糖尿病是一种慢性代谢性疾病，其特征是血糖水平持续高于正常值。"}, {"title": "糖尿病的类型",
 "description": "糖尿病主要分为1型和2型，此外还有其他类型的糖尿病，如妊娠糖尿病等。"}]}, {"title": "糖尿病的病因", "content": [{"title": "遗传因素", "description": "遗传因素在糖尿病的发病中起着重要作用
"}, {"title": "生活方式因素", "description": "不良的饮食习惯、缺乏运动、肥胖等生活方式因素会增加糖尿病的风险。"}, {"title": "环境因素", "description": "环境因素，如病毒感染、化学物质等，也可能导致糖
尿病的发生。"}]}, {"title": "糖尿病的症状", "content": [{"title": "多尿", "description": "糖尿病患者常常出现多尿现象，这是由于高血糖导致肾脏过滤尿液增多。"}, {"title": "多饮", "description": "糖尿病患
者由于多尿，常常感到口渴，需要频繁饮水。"}, {"title": "多食", "description": "糖尿病患者由于能量消耗增加，常常感到饥饿，需要频繁进食。"}, {"title": "体重减轻", "description": "糖尿病患者由于能量消耗增
加，体重可能会减轻。"}, {"title": "视力模糊", "description": "高血糖可能导致视力模糊，这是由于血糖水平影响眼睛晶状体的形态。"}]}, {"title": "糖尿病的诊断", "content": [{"title": "血糖检测", "descriptio
n": "血糖检测是诊断糖尿病的主要方法，包括空腹血糖、餐后血糖等。"}, {"title": "糖耐量测试", "description": "糖耐量测试可以评估胰岛素的作用和血糖的调节能力。"}, {"title": "糖化血红蛋白测试", "description
": "糖化血红蛋白测试可以反映过去3个月内的平均血糖水平。"}]}, {"title": "糖尿病的治疗", "content": [{"title": "饮食治疗", "description": "合理的饮食治疗对于控制血糖水平至关重要。"}, {"title": "运动治疗"
, "description": "规律的运动可以帮助控制体重、改善胰岛素敏感性，从而有助于控制血糖水平。"}, {"title": "药物治疗", "description": "药物治疗是糖尿病治疗的重要手段，包括胰岛素、磺脲类药物等。"}, {"title":
 "血糖监测", "description": "血糖监测可以帮助糖尿病患者了解自己的血糖水平，及时调整饮食和运动计划。"}]}, {"title": "糖尿病的并发症", "content": [{"title": "心血管疾病", "description": "糖尿病患者患心血
疾病的风险较高，包括冠心病、心肌梗死等。"}, {"title": "肾脏疾病", "description": "糖尿病患者患肾脏疾病的风险较高，如糖尿病肾病。"}, {"title": "神经病变", "description": "糖尿病患者可能发生神经病变，
导致感觉异常、疼痛等。"}, {"title": "视网膜病变", "description": "糖尿病患者患视网膜病变的风险较高，可能导致视力下降甚至失明。"}, {"title": "足部并发症", "description": "糖尿病患者患足部并发症的风险较 高，如足部感染、溃疡等。"}]}]}]}
'''
print(raw_json )


# 使用 json.loads 解析 JSON 字符串
try:
    data = json.loads(raw_json)
    print("解析成功:", data)
except json.JSONDecodeError as e:
    print("解析失败:", e)