from __future__ import annotations
from typing import overload, NamedTuple
from numpy import ndarray
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
  
class Cylinder(Shape):
  def __init__(
    self,
    radius: float,
    height: float,
    mass: float,
    m_dot: float,
    start_time: float,
    stop_time: float,
    position: ndarray,
    velocity: ndarray,
    attitude: Quaternion,
    angular_velocity: ndarray
  ):
    super().__init__(
      mass,
      m_dot,
      start_time,
      stop_time,
      position,
      velocity,
      attitude,
      angular_velocity
    )
    
    self.dims = CylinderDims(radius=radius, height=height)


class CylinderDims(NamedTuple):
  radius: float
  height: float