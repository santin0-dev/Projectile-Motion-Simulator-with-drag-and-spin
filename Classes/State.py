Vector2 = tuple[float, float]

class State:
    def __init__(
        self,
        time: float,
        position: Vector2,
        velocity: Vector2,
        acceleration: Vector2 = (0.0, 0.0)
    ):
        self.time = time
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration