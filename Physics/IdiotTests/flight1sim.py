from numpy import array, ndarray, pi, std, mean, sign
import matplotlib.pyplot as plt
from pandas import read_csv
from numpy.random import normal as random_normal
from typing import Tuple

METERS_TO_FEET = 3.28084
M_INITIAL = 0.641

data_dir = "./Physics/IdiotTests/EstesE9.csv"

data = read_csv(data_dir)
times = data["Time (s)"].to_numpy()
thrusts = data["Thrust (N)"].to_numpy()

slopes = []
intercepts = []

for i in range(len(times) - 1):
  slopes.append((thrusts[i + 1] - thrusts[i]) / (times[i + 1] - times[i]))
  intercepts.append(thrusts[i])

rho = 1.28144
g = 9.8
m = M_INITIAL
dm = 0.036 / 3.1
Cd = 0.5
A = 0.037 ** 2 * pi

δT = 0.05

def T(t) -> float:
  for i in range(len(times) - 1):
    if t >= times[i] and t < times[i + 1]:
      # incorporate monte carlo δT% thrust deviation from uncertainty in motor thrust performance
      return (slopes[i] * (t - times[i]) + intercepts[i]) * (1 + δT * random_normal())
  
  return 0.0

def f(r, t) -> ndarray:
  v = r[1]
  a = (-m * g - sign(v) * 0.5 * rho * Cd * A * v ** 2 + T(t)) / m
  return array([v, a], float)

def RK4(f, r, t, dt) -> ndarray:
  global m
  k1 = f(r, t)
  k2 = f(r + k1 * dt / 2, t + dt / 2)
  k3 = f(r + k2 * dt / 2, t + dt / 2)
  k4 = f(r + k3, t + dt)
  if T(t) > 0.0:
    m -= dm * dt
  return dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6

def simulation_loop(plot: bool = False) -> Tuple[float, float]:
  """ calculates equations of motion solution for a rocket with changing mass

  Returns:
      Tuple[float, float]: max altitude in feet, time of flight in seconds
  """
  t_list = []
  y_list = []
  v_list = []
  global m
  t = 0.0
  tf = 1.0
  dt = 1e-3
  r = array([0.0, 0.0], float)
  m = M_INITIAL

  while (t < tf or r[0] > 0.0):
    t_list.append(t)
    y_list.append(r[0])
    v_list.append(r[1])

    dr = RK4(f, r, t, dt)
    if t < 0.2 and dr[1] < 0.0:
      dr = array([0.0, 0.0], float)

    r += dr
    t += dt

  #print(f"Final mass (kg): {m:.3f}")
  #print(f"Maximum altitude (meters): {max(y_list):.2f}")
  #print(f"Maximum altitude (ft): {max(y_list) * METERS_TO_FEET:.2f}")
  #print()
  
  if plot:
    plt.plot(t_list, [_y * METERS_TO_FEET for _y in y_list])
    plt.ylabel("Altitude (ft)")
    plt.xlabel("Time (s)")
    plt.show()
  
  return max(y_list) * METERS_TO_FEET, t

if __name__ == "__main__":
  runs = 100
  alts = []
  ts = []
  for _ in range(runs):
    #print(f"Finished iteration #{_ + 1}")
    alt, _t = simulation_loop()
    alts.append(alt)
    ts.append(_t)
  
  simulation_loop(True)
  
  print(f"Maximum altitude (ft): {mean(alts):.3f} +/- {std(alts):.3f}")
  print(f"Time of flight (s): {mean(ts):.3f} +/- {std(ts):.3f}")