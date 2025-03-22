from __future__ import annotations
from typing import overload, NamedTuple, List
from numpy import ndarray, array
from abc import ABC, abstractmethod
from Quaternion import Quaternion


X, Y, Z = 0, 1, 2

class Shape(ABC):
  # for numpy, we beat it's array priority to use our custom summation tool
  __array_priority__ = 1000
  
  id: int = 0
  
  # body frame properties of the object
  
  # dynamic properties
  pos: ndarray
  linv: ndarray
  att: Quaternion
  angv: ndarray
  I: ndarray # this is the inertia tensor for the shape and only updates when mass changes
  
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
  
  def __m__(self, t: float) -> float:
    if t > self.start_time and t <= self.stop_time:
      return self.m - self.m_dot * (t - self.start_time)
    elif t > self.stop_time:
      return self.m - self.m_dot * (self.stop_time - self.start_time)
    else:
      return self.m
  
  @abstractmethod
  def get_i(self, t: float):
    return self.I
  
  @abstractmethod
  def __str__(self) -> str:
    return f"Shape"
  
  @overload
  def __add__(self, other: Shape) -> ndarray: ...
  
  @overload
  def __add__(self, other: ndarray) -> ndarray: ...
  
  def __add__(self, other: Shape | ndarray) -> ndarray:
    if isinstance(other, Shape):
      return self.i + other.i
    elif isinstance(other, ndarray):
      if _is3x3(other):
        return self.i + other
      else:
        return ValueError("Cannot add array to Shape if not 3x3!")
    else:
      return NotImplemented("Cannot add Shape to other type than Shape!")
  
  @overload
  def __radd__(self, other: Shape) -> ndarray: ...
  
  @overload
  def __radd__(self, other: ndarray) -> ndarray: ...
  
  def __radd__(self, other: Shape | ndarray) -> ndarray:
    if isinstance(other, Shape):
      return self.i + other.i
    elif isinstance(other, ndarray):
      if _is3x3(other):
        return self.i + other
      else:
        return ValueError("Cannot add array to Shape if not 3x3!")
    else:
      return NotImplemented("Cannot add Shape to other type than Shape!")
  
  def __seti__(self, t: float, cg: ndarray = array([0.0, 0.0, 0.0])) -> None:
    coord = self.pos - cg
    m = self.__m__(t=t)
    IXX = m * (coord[Y] ** 2 + coord[Z] ** 2)
    IYY = m * (coord[X] ** 2 + coord[Z] ** 2)
    IZZ = m * (coord[X] ** 2 + coord[Y] ** 2)
    IXY = IYX = m * (-coord[X] * coord[Y])
    IXZ = IZX = m * (-coord[Z] * coord[X])
    IYZ = IZY = m * (-coord[Y] * coord[Z])
    
    self.i = self.get_i(t=t) + array([
      [IXX, IXY, IXZ],
      [IYX, IYY, IYZ],
      [IZX, IZY, IZZ]
    ], dtype=float)

def _is3x3(a: ndarray) -> bool:
  if isinstance(a, ndarray):
    if a.shape == (3, 3):
      return True
    else:
      return False
  return False

def cm(shapes: List[Shape]) -> ndarray:
  """ computes the center of mass from the coordinate system frame of the rigid body

  Args:
      shapes (List[Shape]): all body components

  Returns:
      ndarray: center of mass x, y, z
  """
  _mass_times_coord = array([0.0, 0.0, 0.0])
  _mass = 0.0
  for shape in shapes:
    _mass_times_coord += shape.m * shape.pos
    _mass += shape.m
  
  return _mass_times_coord / _mass