from Classes import projectile, State, Environment
import math

Vector2 = tuple[float, float]

class Simulate():


  def __init__(
    self,
    proj: projectile,
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
                   * self.proj.drag_coef              # how aerodynamicis the projectile
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


  def run():

  def calculate_summary():





  