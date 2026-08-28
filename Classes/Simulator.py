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

    return (net_fx, net_fy)


    



  def calculate_acceleration():

  def advance_epoch():

  def run():

  def calculate_summary():





  