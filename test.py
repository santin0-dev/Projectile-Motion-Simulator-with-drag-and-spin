  # def store_values(self) -> None:
  #   file_path = Path(__file__).parent/"log.csv"

  #   header = ["Launch Speed", "Launch Angle", "Gravity", "Flight Time", "Max Height", "Max Range"]
  #   log = []

  #   if os.path.exists(file_path):
  #     with open (file_path, "a") as file:
  #       writer = csv.writer(file)
  #       writer.writerow(log)
  #   else:
  #     with open(file_path, "w") as file:
  #       writer = csv.writer(file)
  #       writer.writerow(header)
  #       writer.writerow(log)


Vector2 = tuple[float, float]

def calculate_forces(mass, gravity) -> Vector2:
    gravity_fx = 0.0
    gravity_fy = -(mass * gravity)

    return [gravity_fx, gravity_fy]






def calculate_acceleration(mass, net_force: Vector2) -> Vector2:
    if mass <= 0:
        raise ValueError("Projectile mass must be greater than zero.")
        
    net_fx = net_force[0]
    net_fy = net_force[1]

    acceleration_x = net_fx / mass
    acceleration_y = net_fy / mass

    return (acceleration_x, acceleration_y)


print(f"gravitational force: {calculate_forces(2, 9.80665)}")

print(f"acceleration vector: {calculate_acceleration(2,calculate_forces(2, 9.80665) )}")