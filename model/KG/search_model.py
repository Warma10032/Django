from typing import Tuple, Optional, List,Dict

from model.model_base import Modelbase
from model.model_base import ModelStatus

import ahocorasick as pyahocorasick
from model.KG.data_utils import NodeEntities

from collections import namedtuple

FIELD_NAMES = {"name"}
_Value = namedtuple("_Value", (fn for fn in FIELD_NAMES))


class EntitySearcher(Modelbase):

    def __init__(self, *args, **krgs):
        super().__init__(*args, **krgs)
        self._node_entities = NodeEntities()
        self._search_key = "name"
        self.build()

    def build(self, *args, **kwargs):
        self._model_status = ModelStatus.BUILDING

        try:
            self._build_model()
        except Exception as e:
            self._model_status = ModelStatus.FAILED
            return

        self._model_status = ModelStatus.READY

    def _build_model(self, *args, **kwargs):
        automaton = pyahocorasick.Automaton()

        # 在这里的self._node_entities 包含图数据库的节点信息
        for i, entity in enumerate(self._node_entities()):
            # 从字典 entity 中提取 FIELD_NAMES 对应的值
            # values = [entity[fn] for fn in FIELD_NAMES]  # 通过 FIELD_NAMES 获取对应的值
            # value = _Value(*values)
            automaton.add_word(entity[self._search_key], (i, entity))

        automaton.make_automaton()

        self._model = automaton

    def search(self, query: str) -> Tuple[Optional[List[Dict]]]:

        results = []
        for end_index, (insert_order, original_value) in self._model.iter(query):
            results.append(original_value)

        return results


INSTANCE = EntitySearcher()
