import math
import csv
import os

class Projectile():

  # Values
  earth_gravity = 9.80665

  mass: float | None = None
  launch_speed: float | None = None
  launch_angle: float | None = None
  gravity: float | None = None

  # Trajectory values
  time_of_flight: float | None = None
  maximum_height: float | None = None
  horizontal_reach: float | None = None # aka "Range"
  
  def __init__(self, initial_speed: float, mass: float, angle: float, gravity: float) -> None:
    self.launch_speed = initial_speed
    self.mass = mass
    self.launch_angle = angle
    self.gravity = gravity
  
  # in meters
  def calculate_range(self) -> float:
    self.horizontal_reach = ( self.launch_speed**2 
                                * math.sin(2*math.radians(self.launch_angle)) 
                                / self.earth_gravity)
    return self.horizontal_reach

  # in meters
  def calculate_max_height(self) -> float:
    self.maximum_height = ( self.launch_speed**2 
              * math.sin(math.radians(self.launch_angle))**2 
              / (2*self.earth_gravity))
    return self.maximum_height

  # in seconds
  def calculate_flight_time(self) -> float:
    self.time_of_flight = ( 2 * self.launch_speed 
                    * math.sin(math.radians(self.launch_angle)) 
                    / self.earth_gravity)
    return self.time_of_flight

  def store_values(self) -> None:
    file_path = "log.csv"
    writer = csv.writer(file)

    header = ["Launch Speed", "Launch Angle", "Gravity", "Flight Time", "Max Height", "Max Range"]
    log = [self.launch_speed, self.launch_angle, self.earth_gravity, self.time_of_flight, self.maximum_height, self.horizontal_reach]

    if os.path.exists(file_path):
      with open (file_path, "a") as file:
        writer.writerow(log)
    else:
      with open(file_path, "w") as file:
        writer.writerow(header)

    

