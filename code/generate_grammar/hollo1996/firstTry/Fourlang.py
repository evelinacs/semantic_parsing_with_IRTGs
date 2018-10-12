from enum import Enum
class idGenerator:
    id=-1
    @classmethod
    def auto(cls):
        cls.id+=1
        return cls.id


class Fourlang(Enum):
    ZeroTo = idGenerator.auto()
    UnderTo = idGenerator.auto()
    Zero = idGenerator.auto()
    OneTo_ZeroBack = idGenerator.auto()
    TwoTo = idGenerator.auto()
    OneBack__TwoTo = idGenerator.auto()
    OneBack_at_TwoTo = idGenerator.auto()
    OneBack_has_TwoTo = idGenerator.auto()
    ZeroCompound = idGenerator.auto()
    ZeroFlat = idGenerator.auto()
    _None = idGenerator.auto()
