
from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int

@dataclass
class Renderable:
    symbol: str
    color: str

@dataclass
class Combat:
    current_hp: int
    max_hp: int
    attack: int
    defense: int

@dataclass
class AI:
    pass