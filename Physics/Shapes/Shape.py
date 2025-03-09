from __future__ import annotations
from typing import overload, NamedTuple, List
from numpy import ndarray, array
from abc import ABC, abstractmethod
from Quaternion import Quaternion

class Shape(ABC):
  id: int = 0
  
  # body frame properties of the object
  
  # dynamic properties
  pos: ndarray
  linv: ndarray
  att: Quaternion
  angv: ndarray
  
  m_dot: float
  start_time: float
  stop_time: float
  
  # static properties
  m: float
  i: ndarray
  cm: ndarray
  
  # design properties
  dims: NamedTuple
  
  @abstractmethod
  def __init__(
    self,
    mass: float,
    m_dot: float,
    start_time: float,
    stop_time: float,
    position: ndarray,
    velocity: ndarray,
    attitude: Quaternion,
    angular_velocity: ndarray
  ):
    Shape.id += 1
    self.m = mass
    self.m_dot = m_dot
    self.start_time = start_time
    self.stop_time = stop_time
    self.pos = position
    self.linv = velocity
    self.att = attitude
    self.angv = angular_velocity
  
  @abstractmethod
  def __str__(self) -> str:
    return f"Shape"


def cm(shapes: List[Shape]) -> ndarray:
  """ computes the center of mass from the coordinate system frame of the rigid body

  Args:
      shapes (List[Shape]): all body components

  Returns:
      ndarray: center of mass x, y, z
  """
  _mass_times_coord = array([0.0, 0.0, 0.0])
  _coord = array([0.0, 0.0, 0.0])
  for shape in shapes:
    _mass_times_coord += shape.m * shape.pos
    _coord += shape.pos
  
  return _mass_times_coord / _coord