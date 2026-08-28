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


print(f"gravitational force: {calculate_forces(2, 9.80665)}")