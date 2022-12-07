from enum import Enum
from typing import Optional, List


# these are our main groups in the ml studio menu
class Kind(Enum):
    DATA_MANIPULATION = "dataManipulation"
    DATA_SAMPLING = "dataSampling"
    DATA_TRANSFORMATION = "dataTransformation"
    MACHINE_LEARNING = "machineLearning"
    MODEL_EVALUATION = "modelEvaluation"
    INCREMENTAL_LEARNING = "incrementalLearning"
    NO_INPUT = "noInput"


# these are our subgroups groups in the ml studio menu
class SubKind(Enum):
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    CLUSTERING = "clustering"
    TOP = "top"
    CLASSIC = "classic"


class TypeEnum(Enum):
    DATA = "data"
    MODEL = "model"


class Port:
    is_output: bool
    type: TypeEnum

    def __init__(self, is_output: bool, type: TypeEnum) -> None:
        self.is_output = is_output
        self.type = type


class Property:
    display_name: str
    name: str
    type: str
    value: str
    lookup: Optional[List[str]]

    def __init__(self, display_name: str, name: str, type: str, value: "", lookup: Optional[List[str]]) -> None:
        self.display_name = display_name
        self.name = name
        self.type = type
        self.value = value
        self.lookup = lookup


class ModelType(Enum):
    CLUSTER = 'Cluster',
    CLASSIFIER = 'Classifier',
    PRETRAINED = 'Pretrained'


class Node:
    desc: str
    name: str
    ports: List[Port]
    properties: List[Property]
    type: str
    kind: Optional[Kind]
    model_type: Optional[ModelType]

    def __init__(self, desc: str, name: str, ports: List[Port], properties: List[Property], type: str,
                 kind: Optional[Kind], model_type: Optional[ModelType]) -> None:
        self.desc = desc
        self.name = name
        self.ports = ports
        self.properties = properties
        self.type = type
        self.kind = kind
        self.model_type = model_type

    def get_default_values(self):
        values: {}
        for p in self.properties:
            values[p.name] = p.value

        return values


class Group:
    name: str
    icon_name: str
    nodes: List[Node] = []

    def __init__(self, name: str, icon_name: str) -> None:
        self.name = name
        self.icon_name = icon_name


class MenuGroup:
    background_color: str = '#ffffff'
    icon_color: str = '#000000'
    icon_name: str
    name: str
    nodes: List[Node] = []
    groups: Optional[List[Group]] = []

    def __init__(self, icon_name: str, name: str ) -> None:
        self.icon_name = icon_name
        self.name = name

class Mlmenu:
    groups: List[MenuGroup]

    def __init__(self, groups: List[MenuGroup]) -> None:
        self.groups = groups
