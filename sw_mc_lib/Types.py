from enum import Enum


class _Enum(Enum):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


class SignalType(_Enum):
    """
    Signal types
    """

    Boolean = 0
    Number = 1
    Composite = 5
    Video = 6
    Audio = 7


class NodeMode(_Enum):
    """
    Modes of nodes (in/out connections)
    """

    Output = 0
    Input = 1


class TooltipMode(_Enum):
    """
    Modes of Tooltips, depending on the error/signal input
    """

    Always = 0
    IfOn = 1
    IfOff = 2


class PulseMode(_Enum):
    """
    Modes of the Pulse Component, note that OffToOn is the default mode
    """

    OnToOff = 0
    OffToOn = 1
    Always = 2


class TimerUnit(_Enum):
    """
    Units of timer Components
    """

    Seconds = 0
    Ticks = 1


class ComponentType(_Enum):
    """
    Types of Components and their respective ids
    """

    NOT = 0
    AND = 1
    OR = 2
    XOR = 3
    NAND = 4
    NOR = 5
    Add = 6
    Subtract = 7
    Multiply = 8
    Divide = 9
    ArithmeticFunction3In = 10
    Clamp = 11
    Threshold = 12
    MemoryRegister = 13
    Abs = 14
    ConstantNumber = 15
    ConstantOn = 16
    GreaterThan = 17
    LessThan = 18
    PropertySlider = 19
    PropertyDropdown = 20
    NumericalJunction = 21
    NumericalSwitchbox = 22
    PIDController = 23
    SRLatch = 24
    JKFlipFlop = 25
    Capacitor = 26
    Blinker = 27
    PushToToggle = 28
    CompositeReadBoolean = 29
    CompositeWriteBooleanDeprecated = 30
    CompositeReadNumber = 31
    CompositeWriteNumberDeprecated = 32
    PropertyToggle = 33
    PropertyNumber = 34
    Delta = 35
    ArithmeticFunction8In = 36
    UpDownCounter = 37
    Modulo = 38
    PIDControllerAdvanced = 39
    CompositeWriteNumber = 40
    CompositeWriteBoolean = 41
    Equal = 42
    TooltipNumber = 43
    TooltipBoolean = 44
    ArithmeticFunction1In = 45
    BooleanFunction4In = 46
    BooleanFunction8In = 47
    Pulse = 48
    TimerTON = 49
    TimerTOF = 50
    TimerRTO = 51
    TimerRTF = 52
    CompositeSwitchbox = 53
    NumberToCompositeBinary = 54
    CompositeBinaryToNumber = 55
    LuaScript = 56
    VideoSwitchbox = 57
    PropertyText = 58
    AudioSwitchbox = 59
