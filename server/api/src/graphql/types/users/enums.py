from enum import StrEnum

import strawberry


@strawberry.enum
class Gender(StrEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"


@strawberry.enum
class Goal(StrEnum):
    MAINTAIN = "MAINTAIN"
    LOSE = "LOSE"
    GAIN = "GAIN"
