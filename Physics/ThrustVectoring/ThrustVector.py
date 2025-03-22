from __future__ import annotations
from numpy import array, sign
from numpy.random import normal as normal_random

DEGREES_TO_RADIANS = 3.141592 / 180.0

class ThrustVector:
  def __init__(self, x: float = 0.0, y: float = 0.0, errorx: float = 0.0, errory: float = 0.0, targetx = 0.0, targety = 0.0, max_rate: float = 90.0):
    self.max_rate = max_rate
    self.x = x
    self.y = y
    self.errorx = errorx
    self.errory = errory
    self.targetx = targetx
    self.targety= targety
  
  def step(self, x: float, y: float, dt: float = 1e-3) -> tuple[float, float]:
    self.targetx = x
    self.targety = y
    self.__move_x__(dt)
    self.__move_y__(dt)
    return self.x, self.y
  
  def copy(self) -> ThrustVector:
    return ThrustVector(self.x, self.y, self.targetx, self.targety, self.max_rate)
  
  def __move_x__(self, dt: float) -> None:
    if abs(r:=(self.targetx - self.x)) <= self.max_rate * dt:
      self.x = self.targetx
    else:
      self.x += sign(r) * self.max_rate * dt
    
    self.x += normal_random() * self.errorx / 1.96
  
  def __move_y__(self, dt: float) -> None:
    if abs(r:=(self.targety - self.y)) <= self.max_rate * dt:
      self.y = self.targety
    else:
      self.y += sign(r) * self.max_rate * dt
    
    self.y += normal_random() * self.errory / 1.96

if __name__ == "__main__":
  t = ThrustVector()
  