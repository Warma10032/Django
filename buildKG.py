from py2neo import Graph, Node, Relationship
import json
from concurrent.futures import ThreadPoolExecutor

# 连接到 Neo4j 数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))


# 定义处理每个 JSON 对象的函数
def process_line(json_data):
    # 使用 merge 确保疾病节点不会重复创建
    disease_node = Node(
        "Disease",
        name=json_data["name"],
        description=json_data["desc"],
        yibao_status=json_data["yibao_status"],
        get_prob=json_data["get_prob"],
        get_way=json_data["get_way"],
        cure_lasttime=json_data["cure_lasttime"],
        cured_prob=json_data["cured_prob"],
        cost_money=json_data["cost_money"],
    )
    graph.merge(disease_node, "Disease", "name")  # 使用 "name" 作为唯一标识符
    

    # 创建与疾病相关的症状节点并建立关系
    for symptom in json_data["symptom"]:
        symptom_node = Node("Symptom", name=symptom)
        graph.merge(symptom_node, "Symptom", "name")  # 确保唯一性
        graph.merge(Relationship(disease_node, "症状", symptom_node))

    # 创建伴随疾病节点并建立关系
    for accompany in json_data["acompany"]:
        accompany_node = Node("Disease", name=accompany)
        graph.merge(accompany_node, "Disease", "name")  # 确保唯一性
        graph.merge(Relationship(disease_node, "伴随", accompany_node))

    # 创建治疗方式节点并建立关系
    for cure_way in json_data["cure_way"]:
        cure_way_node = Node("Treatment", name=cure_way)
        graph.merge(cure_way_node, "Treatment", "name")
        graph.merge(Relationship(disease_node, "治疗方法", cure_way_node))

    # 创建检查方式节点并建立关系
    for check in json_data["check"]:
        check_node = Node("Check", name=check)
        graph.merge(check_node, "Check", "name")
        graph.merge(Relationship(disease_node, "检查方式", check_node))

    # 创建科室节点并建立关系
    for department in json_data["cure_department"]:
        department_node = Node("Department", name=department)
        graph.merge(department_node, "Department", "name")
        graph.merge(Relationship(disease_node, "治疗科室", department_node))


    print(f"疾病 '{json_data['name']}' 和相关节点已成功导入 Neo4j")


# 多线程读取和处理 JSONL 文件
def process_jsonl_in_parallel(file_path, max_workers=4):
    with open(file_path, "r", encoding="utf-8") as file:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 为每一行创建任务，提交到线程池中
            futures = [executor.submit(process_line, json.loads(line)) for line in file]

            # 等待所有线程完成
            for future in futures:
                future.result()  # 检查是否有异常发生


if __name__ == "__main__":
    # 执行多线程导入
    process_jsonl_in_parallel("medical.jsonl", max_workers=8)
