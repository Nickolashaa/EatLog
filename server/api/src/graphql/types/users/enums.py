from enum import Enum

import strawberry


@strawberry.enum
class Gender(Enum):
    MALE = "male"
    FEMALE = "female"


@strawberry.enum
class Goal(Enum):
    MAINTAIN = "maintain"
    LOSE = "lose"
    GAIN = "gain"
