class Microcontroller:
    def __init__(
        self,
        name: str,
        description: str,
        width: int,
        length: int,
        id_counter: int,
        id_counter_node: int,
    ):
        self.name: str = name
        self.description: str = description
        self.width: int = width
        self.length: int = length
        self.id_counter: int = id_counter
        self.id_counter_node: int = id_counter_node
