import math

from Classes.Projectile import Projectile
from Classes.Environment import Environment
from Classes.State import State
from Classes.Simulator import Simulator


def main() -> None:
    #===== LAUNCH SETTINGS =====
    launch_speed = 40.0       # m/s
    launch_angle_deg = 40.0   # degrees
    initial_height = 1.8      # metres

    launch_angle_rad = math.radians(launch_angle_deg)

    initial_vx = launch_speed * math.cos(launch_angle_rad)
    initial_vy = launch_speed * math.sin(launch_angle_rad)

    radius = 0.0366

    # Create Projectile
    projectile = Projectile( 
        mass = 0.145,                  # kg
        area = math.pi * radius**2,    # front area in m^2
        drag_coefficient = 0.47,
        radius = radius,
        spin_rad_s = 0.0)                    # rad/s not used for now

    # Create Environment
    environment = Environment(
        gravity=9.80665,              # m/s²
        air_density=1.225,            # kg/m³ at sea level
        wind=(0.0, 0.0),              # wind velocity vector, m/s
        latitude_deg=14.6,                # degrees
        altitude_m=0.0                  # metres
    )
    # Create initial State
    initial_state = State(
        time=0.0,
        position=(0.0, initial_height),
        velocity=(initial_vx, initial_vy),
        acceleration=(0.0, 0.0)
    )


    # Create Simulator
    simulator = Simulator(projectile, environment, initial_state)

    history = simulator.run()
    summary = simulator.calculate_summary(history)

    simulator.store_epoch_history(history)
    simulator.store_summary(summary)


if __name__ == "__main__":
    main()