from dataclasses import dataclass,field
from pathlib import Path

from py2neo import Node
from kg.Graph import GraphDao


@dataclass
class NodeEntities(object):
    # 该类负责与Graph类交互，获取节点信息

    dao: GraphDao = field(default_factory=lambda: GraphDao(), init=True, compare=False)

    # 获取节点
    def get_entities_iterator(self) -> Node:
        # 通过GraphDao去连接
        meta_node = self.dao.query_meta_node()
        nodes = self.dao.query_node('唐')
        node_list=[]
        for node in nodes:
            node_dict = {
            'labels': '-'.join(node.labels),  # 将标签用 "-" 连接
            **dict(node)  # 解包节点的属性
             }
            node_list.append(node_dict)
            

        return node_list
        
       
    def __call__(self, *args, **kwargs):
        return self.get_entities_iterator()
