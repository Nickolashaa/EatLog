from typing import TypedDict

from ..profile.types import ProfileBase


class UserUpdateParams(TypedDict):
    uuid: str
    profile: ProfileBase
