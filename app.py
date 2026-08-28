from Classes.projectile import Projectile

ball = Projectile(10, 1, 30, 9.8)

flight_t = ball.calculate_flight_time()
max_h = ball.calculate_max_height()
reach = ball.calculate_range()


print(f"Time of flight: {flight_t:.2f}s",
      f"\nMax Height: {max_h:.2f} meters",
      f"\nMax Reach: {reach:.2f} meters"
)

ball.store_values()



isrunning = True

while isrunning:
      initial_speed = None
      gravity = None
      angle = None
      mass = None

      print("====================")

      while True:
            
            try:
                  initial_speed = float(input("Enter initial speed:  "))
                  mass = float(input("Enter projectile mass: "))
                  angle = float(input("Enter angle of launch: "))
                  gravity = float(input("Enter specific gravity [default earth gravity]: "))
            except ValueError:
                  print("Values should be numerical")
                  
            print(f"initial speed: {initial_speed}",
                  f"mass: {mass}",
                  f"angle: {angle}",
                  f"gravity: {gravity}")
