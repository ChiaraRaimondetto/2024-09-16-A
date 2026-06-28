from dataclasses import dataclass

from model.state import State


@dataclass
class Arco:
    s1:State
    s2:State
    peso:int
