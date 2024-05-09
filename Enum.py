from enum import Enum
class EraType(Enum):
    ERA_ANCIENT = "ERA_ANCIENT"
    ERA_CLASSICAL = "ERA_CLASSICAL"
    ERA_MEDIEVAL = "ERA_MEDIEVAL"
    ERA_RENAISSANCE = "ERA_RENAISSANCE"
    ERA_INDUSTRIAL = "ERA_INDUSTRIAL"
    ERA_MODERN = "ERA_MODERN"
    ERA_ATOMIC = "ERA_ATOMIC"
    ERA_INFORMATION = "ERA_INFORMATION"
    ERA_FUTURE = "ERA_FUTURE"

class CivVICheckType(Enum):
    TECH = "TECH"
    CIVIC = "CIVIC"
    PROGRESSIVE_DISTRICT = "PROGRESSIVE_DISTRICT"