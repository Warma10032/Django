from config.config import Config
from py2neo import Graph, Node, NodeMatcher, RelationshipMatcher, ConnectionUnavailable

class GraphDao(object):

    def __init__(self):
        # 读取yaml配置
        self.__url = Config.get_instance().get_with_nested_params("database", "neo4j", "url")
        self.__username = Config.get_instance().get_with_nested_params("database", "neo4j", "username")
        self.__password = Config.get_instance().get_with_nested_params("database", "neo4j", "password")
        self.__connect_graph()
        self.__meta_node_id = 'meta-001'

        # 创建节点匹配器
        self.__node_matcher = NodeMatcher(self.__graph) if self.__graph else None

        # 创建关系匹配器
        self.__relationship_matcher = RelationshipMatcher(self.__graph) if  self.__graph else None

    @staticmethod
    def ensure_connection(function):
        def wrapper(*args, **kwargs):
            if not args[0].__graph:
                return None
            return function(*args, **kwargs)

        return wrapper

    def __connect_graph(self):
        try:
            self.__graph = Graph(self.__url, auth=(self.__username, self.__password))
        except ConnectionUnavailable as e:
            self.__graph = None
    
    @ensure_connection
    def query_relationship_by_2person_name(self, first_person, second_person):
        rel = self.__graph.run(
            f"match(:`人物`{{name:'{first_person}'}})-[r]-(:`人物`{{name:'{second_person}'}}) return r, type(r)").data()
        return rel

    # 请求meta_node
    @ensure_connection
    def query_meta_node(self):
        return self.__node_matcher.match('Meta', id=self.__meta_node_id).first()
    
    @ensure_connection
    def query_node(self, *label, **properties):
        return self.__node_matcher.match(*label, **properties)
