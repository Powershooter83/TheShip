from enum import Enum


class EnergyComponentEnum(Enum):
    THRUSTER_BACK = "thruster_back"
    THRUSTER_FRONT = "thruster_front"
    THRUSTER_FRONT_LEFT = "thruster_front_left"
    THRUSTER_FRONT_RIGHT = "thruster_front_right"
    THRUSTER_BOTTOM_LEFT = "thruster_bottom_left"
    THRUSTER_BOTTOM_RIGHT = "thruster_bottom_right"
    LASER = "laser"
    CARGO_BOT = "cargo_bot"
    SCANNER = "scanner"
    JUMPDRIVE = "jumpdrive"

