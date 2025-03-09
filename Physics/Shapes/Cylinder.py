from Shape import *

class Cylinder(Shape):
  def __init__(
    self,
    radius: float,
    height: float,
    mass: float,
    m_dot: float,
    start_time: float,
    stop_time: float,
    position: ndarray = array([0.0, 0.0, 0.0]),
    velocity: ndarray = array([0.0, 0.0, 0.0]),
    attitude: Quaternion = Quaternion(),
    angular_velocity: ndarray = array([0.0, 0.0, 0.0])
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
    
    IXX = IYY = self.m * self.dims.height ** 2 / 12 + self.m * self.dims.radius ** 2 / 4
    IZZ = self.m * self.dims.radius ** 2 / 2
    self.i = array([
      [IXX, 0, 0],
      [0, IYY, 0],
      [0, 0, IZZ]
    ], dtype=float)
  
  def __str__(self) -> str:
    return f"Cylinder"


class CylinderDims(NamedTuple):
  radius: float
  height: float