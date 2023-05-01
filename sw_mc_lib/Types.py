from enum import Enum


class _Enum(Enum):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


class SignalType(_Enum):
    """
    Signal types
    """

    Boolean: int = 0
    Number: int = 1
    Composite: int = 5
    Video: int = 6
    Audio: int = 7


class NodeMode(_Enum):
    """
    Modes of nodes (in/out connections)
    """

    Output: int = 0
    Input: int = 1


class TooltipMode(_Enum):
    """
    Modes of Tooltips, depending on the error/signal input
    """

    Always: int = 0
    IfOn: int = 1
    IfOff: int = 2


class PulseMode(_Enum):
    """
    Modes of the Pulse Component, note that OffToOn is the default mode
    """

    OnToOff: int = 0
    OffToOn: int = 1
    Always: int = 2


class TimerUnit(_Enum):
    """
    Units of timer Components
    """

    Seconds: int = 0
    Ticks: int = 1


class ComponentType(_Enum):
    """
    Types of Components and their respective ids
    """

    NOT: int = 0
    AND: int = 1
    OR: int = 2
    XOR: int = 3
    NAND: int = 4
    NOR: int = 5
    Add: int = 6
    Subtract: int = 7
    Multiply: int = 8
    Divide: int = 9
    ArithmeticFunction3In: int = 10
    Clamp: int = 11
    Threshold: int = 12
    MemoryRegister: int = 13
    Abs: int = 14
    ConstantNumber: int = 15
    ConstantOn: int = 16
    GreaterThan: int = 17
    LessThan: int = 18
    PropertySlider: int = 19
    PropertyDropdown: int = 20
    NumericalJunction: int = 21
    NumericalSwitchbox: int = 22
    PIDController: int = 23
    SRLatch: int = 24
    JKFlipFlop: int = 25
    Capacitor: int = 26
    Blinker: int = 27
    PushToToggle: int = 28
    CompositeReadBoolean: int = 29
    CompositeWriteBooleanDeprecated: int = 30
    CompositeReadNumber: int = 31
    CompositeWriteNumberDeprecated: int = 32
    PropertyToggle: int = 33
    PropertyNumber: int = 34
    Delta: int = 35
    ArithmeticFunction8In: int = 36
    UpDownCounter: int = 37
    Modulo: int = 38
    PIDControllerAdvanced: int = 39
    CompositeWriteNumber: int = 40
    CompositeWriteBoolean: int = 41
    Equal: int = 42
    TooltipNumber: int = 43
    TooltipBoolean: int = 44
    ArithmeticFunction1In: int = 45
    BooleanFunction4In: int = 46
    BooleanFunction8In: int = 47
    Pulse: int = 48
    TimerTON: int = 49
    TimerTOF: int = 50
    TimerRTO: int = 51
    TimerRTF: int = 52
    CompositeSwitchbox: int = 53
    NumberToCompositeBinary: int = 54
    CompositeBinaryToNumber: int = 55
    LuaScript: int = 56
    VideoSwitchbox: int = 57
    PropertyText: int = 58
    AudioSwitchbox: int = 59
