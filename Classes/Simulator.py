from Classes import projectile, State, Environment

class Simulate():
  def __init__(
    self,
    proj: projectile,
    conditions: Environment,
    initial_state: State
    ):
      self.projectile = proj
      self.conditions = conditions
      self.initial_state = initial_state



  