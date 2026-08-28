class Projectile:
    def __init__(
        self,
        mass: float,
        area: float,
        drag_coefficient: float,
        radius: float,
        spin_rad_s: float = 0.0
    ):
        self.mass = mass
        self.area = area
        self.drag_coefficient = drag_coefficient
        self.radius = radius
        self.spin_rad_s = spin_rad_s