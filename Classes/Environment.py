class Environment:
    STANDARD_GRAVITY = 9.80665

    def __init__(
        self,
        air_density: float,
        wind: Vector2 = (0.0, 0.0),
        gravity: float = STANDARD_GRAVITY,
        latitude_deg: float | None = None,
        altitude_m: float = 0.0
    ):
        self.gravity = gravity
        self.air_density = air_density
        self.wind = wind
        self.latitude_deg = latitude_deg
        self.altitude_m = altitude_m