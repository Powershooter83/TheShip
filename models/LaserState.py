from enum import Enum


class LaserState(Enum):
    IS_MINING = "is_mining"
    IS_COOLING_DOWN = "is_cooling_down"
    IS_ACTIVE = "is_active"
    NOT_FOUND = "not_found"
