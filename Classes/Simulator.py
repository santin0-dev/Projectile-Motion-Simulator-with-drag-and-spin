from .Projectile import Projectile
from .Environment import Environment
from .State import State
import math

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from pathlib import Path
import os
import csv

Vector2 = tuple[float, float]

class Simulator():


  def __init__(
    self,
    proj: Projectile,
    conditions: Environment,
    initial_state: State,
    dt: float = 0.01
    ):
      self.proj = proj
      self.conditions = conditions
      self.initial_state = initial_state
      self.dt = dt


  def calculate_forces(self, state: State) -> Vector2:
    """
      Current velocity + wind
        ↓
      velocity through the air
        ↓
      drag force
        ↓
      add gravity
        ↓
      net force
    
    """

    #===== CALCULATING GRAVITATIONAL FORCE =====
    gravity_fx = 0.0
    gravity_fy = -(self.proj.mass * self.conditions.gravity)

    #===== VELOCITY RELATIVE TO AIR =====
    relative_vx = state.velocity[0] - self.conditions.wind[0]
    relative_vy = state.velocity[1] - self.conditions.wind[1]
  
    relative_speed = math.hypot(relative_vx, relative_vy)

    #===== CALCULATING DRAG FORCE =====
    drag_factor = (0.5
                   * self.conditions.air_density      # how crowded is the air
                   * self.proj.drag_coefficient              # how aerodynamicis the projectile
                   * self.proj.area                   # how much surface is hitting the air
                   * relative_speed                   # how quick is the air passing the proj
                   )

    drag_fx = -drag_factor * relative_vx
    drag_fy = -drag_factor * relative_vy
    
    #===== NET FORCE =====
    net_fx = gravity_fx + drag_fx
    net_fy = gravity_fy + drag_fy

    # net force measured in Newtons
    return (net_fx, net_fy)

  def calculate_acceleration(self, net_force: Vector2) -> Vector2:
    """
    Net force
    ↓
    divide by projectile mass
    ↓
    acceleration vector
    """

    #===== VALIDATING MASS =====
    if self.proj.mass <= 0:
        raise ValueError("Projectile mass must be greater than zero.")

    #===== DECOMPOSING NET FORCE VECTOR =====
    net_fx = net_force[0]
    net_fy = net_force[1]

    #===== CALCULATING ACCELERATION =====
    acceleration_x = net_fx / self.proj.mass
    acceleration_y = net_fy / self.proj.mass

    # Acceleration vector measured in m/s²
    return (acceleration_x, acceleration_y)



  def advance_epoch(self, current_state: State, acceleration: Vector2) -> State:
    """
    Current state + acceleration
    ↓
    update velocity
    ↓
    update position
    ↓
    return next state
    """
    # Position
    current_x = current_state.position[0]
    current_y = current_state.position[1]

    # Velocity
    current_vx = current_state.velocity[0]
    current_vy = current_state.velocity[1]

    # Acceleration
    accel_x = acceleration[0]
    accel_y = acceleration[1]
    


     #===== NEW VELOCITY =====
    new_vx = current_vx + accel_x * self.dt
    new_vy = current_vy + accel_y * self.dt

    #===== NEW POSITION =====
    new_x = current_x + new_vx * self.dt
    new_y = current_y + new_vy * self.dt

    #===== NEW TIME =====
    new_time = current_state.time + self.dt

    #===== NEW STATE =====
    new_state = State(
        time=new_time,
        position=(new_x, new_y),
        velocity=(new_vx, new_vy),
        acceleration=(accel_x, accel_y)
    )

    return new_state


  def run(self) -> list[State]:
    """
    Initial state
    ↓
    calculate net force
    ↓
    calculate acceleration
    ↓
    advance one epoch
    ↓
    store new state
    ↓
    repeat until landing
    """

    #===== INITIALIZING SIMULATION =====
    current_state = self.initial_state
    history = [current_state]

    ground_y = 0.0

    #===== SIMULATION LOOP =====
    while True:

        # Calculate the net force at the current epoch
        net_force = self.calculate_forces(current_state)

        # Convert net force into acceleration
        acceleration = self.calculate_acceleration(net_force)

        # Move the simulation forward by dt
        new_state = self.advance_epoch(
            current_state,
            acceleration
        )

        # ===== PRINT CURRENT EPOCH =====
        # epoch = len(history)

        # speed = math.hypot(
        #     new_state.velocity[0],
        #     new_state.velocity[1]
        # )

        # print(
        #     f"Epoch {epoch:05d} | "
        #     f"Time: {new_state.time:7.3f} s | "
        #     f"Position: ({new_state.position[0]:8.3f}, "
        #     f"{new_state.position[1]:8.3f}) m | "
        #     f"Velocity: ({new_state.velocity[0]:8.3f}, "
        #     f"{new_state.velocity[1]:8.3f}) m/s | "
        #     f"Speed: {speed:7.3f} m/s | "
        #     f"Acceleration: ({new_state.acceleration[0]:7.3f}, "
        #     f"{new_state.acceleration[1]:7.3f}) m/s²"
        # )

        # Store this epoch
        history.append(new_state)

        # Make the new state the current state
        current_state = new_state

        #===== LANDING CHECK =====
        has_reached_ground = (
            current_state.position[1] <= ground_y
            and current_state.velocity[1] < 0
        )

        if has_reached_ground:
            break

   

    return history


  def calculate_summary(self, history: list[State]) -> dict[str, float]:
    """
    Complete epoch history
      ↓
    find highest state
      ↓
    inspect final state
      ↓
    calculate final simulation results
    """

    if not history:
      raise ValueError("Cannot calculate summary from an empty history")

    initial_state = history[0]
    final_state = history[-1]


    heighest_state = max(
        history,
        key = lambda state: state.position[1]
      )

    maximum_height = heighest_state.position[1]
    height_gained = maximum_height - initial_state.position[1]
    time_at_max_height = heighest_state.time

    flight_time = final_state.time - initial_state.time

    horizontal_range = (
      final_state.position[0]  -  initial_state.position[0]
    )

    impact_vx = final_state.velocity[0]
    impact_vy = final_state.velocity[1]

    impact_speed = math.hypot(impact_vx, impact_vy)

    maximum_speed = max(
      math.hypot(
        state.velocity[0],
        state.velocity[1]
      )
      for state in history
    )


    return {
        "flight_time_s": flight_time,
        "maximum_height_m": maximum_height,
        "height_gained_m": height_gained,
        "time_at_max_height_s": time_at_max_height,
        "horizontal_range_m": horizontal_range,
        "impact_velocity_x_mps": impact_vx,
        "impact_velocity_y_mps": impact_vy,
        "impact_speed_mps": impact_speed,
        "maximum_speed_mps": maximum_speed
    }


  def store_summary(self, history_log: dict) -> None:
    file_path = Path(__file__).parent.parent/ "Data" / "log.csv"

    header = ["flight_time_s",
        "maximum_height_m",
        "height_gained_m",
        "time_at_max_height_s",
        "horizontal_range_m",
        "impact_velocity_x_mps",
        "impact_velocity_y_mps",
        "impact_speed_mps",
        "maximum_speed_mps"]


    log = [
        history_log["flight_time_s"],
        history_log["maximum_height_m"],
        history_log["height_gained_m"],
        history_log["time_at_max_height_s"],
        history_log["horizontal_range_m"],
        history_log["impact_velocity_x_mps"],
        history_log["impact_velocity_y_mps"],
        history_log["impact_speed_mps"],
        history_log["maximum_speed_mps"]

    ]

    if os.path.exists(file_path):
      with open (file_path, "a") as file:
        writer = csv.writer(file)
        writer.writerow(log)
    else:
      with open(file_path, "w") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerow(log)







  def store_epoch_history(self, history: list[State]) -> None:
    """
    Complete state history
    ↓
    convert each State into one CSV row
    ↓
    store every simulation epoch
    """

    file_path = Path(__file__).parent.parent / "Data" / "epoch_log.csv"

    header = [
        "epoch",
        "time_s",
        "position_x_m",
        "position_y_m",
        "velocity_x_mps",
        "velocity_y_mps",
        "speed_mps",
        "acceleration_x_mps2",
        "acceleration_y_mps2"
    ]

    # "w" creates a fresh epoch log for each simulation.
    with file_path.open(
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)
        writer.writerow(header)

        #===== WRITING EVERY EPOCH =====
        for epoch, state in enumerate(history):

            speed = math.hypot(
                state.velocity[0],
                state.velocity[1]
            )

            row = [
                epoch,
                state.time,
                state.position[0],
                state.position[1],
                state.velocity[0],
                state.velocity[1],
                speed,
                state.acceleration[0],
                state.acceleration[1]
            ]

            writer.writerow(row)


  def animate_trajectory(
        history: list[State],
        interval_ms: float = 10
    ) -> None:
        """
        Epoch history
        ↓
        display one State per frame
        ↓
        move projectile point
        ↓
        draw trajectory behind it
        ↓
        display epoch values
        """

        #===== VALIDATING HISTORY =====
        if not history:
            raise ValueError("Cannot animate an empty history.")

        #===== EXTRACTING POSITIONS =====
        x_positions = [
            state.position[0]
            for state in history
        ]

        y_positions = [
            state.position[1]
            for state in history
        ]

        #===== CREATING GRAPH =====
        fig, (ax, info_ax) = plt.subplots(
            1,
            2,
            figsize=(12, 6),
            gridspec_kw={
                "width_ratios": [3, 1]
            }
        )

        #===== INFORMATION PANEL =====
        info_ax.axis("off")
        info_ax.set_title("Epoch Values")

        #===== GRAPH BOUNDARIES =====
        x_margin = max(
            (max(x_positions) - min(x_positions)) * 0.05,
            1.0
        )

        y_margin = max(
            (max(y_positions) - min(y_positions)) * 0.10,
            1.0
        )

        ax.set_xlim(
            min(x_positions) - x_margin,
            max(x_positions) + x_margin
        )

        ax.set_ylim(
            min(0.0, min(y_positions)) - y_margin,
            max(y_positions) + y_margin
        )

        #===== GRAPH LABELS =====
        ax.set_title("Projectile Motion Simulation")
        ax.set_xlabel("Horizontal Distance (m)")
        ax.set_ylabel("Height (m)")
        ax.axhline(
            y=0,
            color="black",
            linewidth=1
        )
        ax.grid(True)
        ax.set_aspect(
            "equal",
            adjustable="box"
        )

        #===== TRAJECTORY LINE =====
        trajectory_line, = ax.plot(
            [],
            [],
            color="blue",
            linewidth=2,
            label="Trajectory"
        )

        #===== PROJECTILE POINT =====
        projectile_point, = ax.plot(
            [],
            [],
            marker="o",
            color="red",
            markersize=8,
            linestyle="None",
            label="Projectile"
        )

        #===== EPOCH INFORMATION TEXT =====
        epoch_text = info_ax.text(
            0.05,
            0.95,
            "",
            transform=info_ax.transAxes,
            verticalalignment="top",
            family="monospace",
            fontsize=10
        )

        ax.legend()

        #===== INITIAL FRAME =====
        def initialize():
            trajectory_line.set_data([], [])
            projectile_point.set_data([], [])
            epoch_text.set_text("")

            return (
                trajectory_line,
                projectile_point,
                epoch_text
            )

        #===== UPDATING EACH FRAME =====
        def update(frame_index: int):
            current_state = history[frame_index]

            # Current position
            position_x = current_state.position[0]
            position_y = current_state.position[1]

            # Current velocity
            velocity_x = current_state.velocity[0]
            velocity_y = current_state.velocity[1]

            # Current acceleration
            acceleration_x = current_state.acceleration[0]
            acceleration_y = current_state.acceleration[1]

            # Current speed
            speed = math.hypot(
                velocity_x,
                velocity_y
            )

            #===== UPDATE TRAJECTORY =====
            trajectory_line.set_data(
                x_positions[:frame_index + 1],
                y_positions[:frame_index + 1]
            )

            #===== UPDATE PROJECTILE =====
            projectile_point.set_data(
                [position_x],
                [position_y]
            )

            #===== UPDATE EPOCH VALUES =====
            epoch_text.set_text(
                f"Epoch: {frame_index}\n"
                f"Time:  {current_state.time:8.3f} s\n\n"

                f"Position\n"
                f"  x: {position_x:8.3f} m\n"
                f"  y: {position_y:8.3f} m\n\n"

                f"Velocity\n"
                f"  vx:    {velocity_x:8.3f} m/s\n"
                f"  vy:    {velocity_y:8.3f} m/s\n"
                f"  speed: {speed:8.3f} m/s\n\n"

                f"Acceleration\n"
                f"  ax: {acceleration_x:8.3f} m/s²\n"
                f"  ay: {acceleration_y:8.3f} m/s²"
            )

            return (
                trajectory_line,
                projectile_point,
                epoch_text
            )

        #===== ADJUSTING LAYOUT =====
        plt.tight_layout()

        #===== CREATING ANIMATION =====
        animation = FuncAnimation(
            fig=fig,
            func=update,
            frames=len(history),
            init_func=initialize,
            interval=interval_ms,
            blit=True,
            repeat=False
        )

        # Keep animation referenced until the window closes.
        plt.show()