from Shape import *

class Tube(Shape):
  def __init__(
    self,
    inner_radius: float,
    outer_radius: float,
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
    
    self.dims = TubeDims(inner_radius=inner_radius, outer_radius=outer_radius, height=height)
    
    IXX = IYY = self.m / 12 * (3 * (self.dims.inner_radius ** 2 + self.dims.outer_radius ** 2) + self.dims.height ** 2)
    IZZ = self.m / 2 * (self.dims.inner_radius ** 2 + self.dims.outer_radius ** 2)
    self.I = array([
      [IXX, 0, 0],
      [0, IYY, 0],
      [0, 0, IZZ]
    ], dtype=float)
    
    self.__seti__()
  
  def __str__(self) -> str:
    return f"Tube"
  
  def __mass_changed__(self):
    IXX = IYY = self.m / 12 * (3 * (self.dims.inner_radius ** 2 + self.dims.outer_radius ** 2) + self.dims.height ** 2)
    IZZ = self.m / 2 * (self.dims.inner_radius ** 2 + self.dims.outer_radius ** 2)
    self.I = array([
      [IXX, 0, 0],
      [0, IYY, 0],
      [0, 0, IZZ]
    ], dtype=float)


class TubeDims(NamedTuple):
  inner_radius: float
  outer_radius: float
  height: float