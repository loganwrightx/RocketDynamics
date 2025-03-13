from __future__ import annotations
from numpy import ndarray, array, sin, cos

from Motors.Motor import Motor, AVAILABLE

DEGREES_TO_RADIANS = 3.141592 / 180.0

class ThrustVector:
  def __init__(self, motor: str, x: float = 0.0, y: float = 0.0, targetx = 0.0, targety = 0.0, max_rate: float = 270.0):
    self.motor: Motor = Motor(motor)
    self.max_rate = max_rate
    self.x = x
    self.y = y
    self.targetx = targetx
    self.targety= targety
  
  def step(self, x: float, y: float, dt: float = 0.0) -> None:
    self.targetx = x
    self.targety = y
    self.__move_x__(x, dt)
    self.__move_y__(y, dt)
  
  def force(self, t: float) -> ndarray:
    return self.motor.thrust(t) * array([0, 0, 1.0])
  
  def copy(self) -> ThrustVector:
    return ThrustVector(self.motor.motor, self.x, self.y, self.targetx, self.targety, self.max_rate)
  
  def __move_x__(self, x: float, dt: float) -> None:
    if abs(self.targetx - self.x) < self.max_rate * dt:
      self.x = x
    else:
      self.x -= self.max_rate * dt
  
  def __move_y__(self, y: float, dt: float) -> None:
    if abs(self.targety - self.y) < self.max_rate * dt:
      self.y = y
    else:
      self.y -= self.max_rate * dt

if __name__ == "__main__":
  print(AVAILABLE)
  t = ThrustVector("E9")
  print(t.force(0.5))
  