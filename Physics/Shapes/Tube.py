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
    angular_velocity: ndarray = array([0.0, 0.0, 0.0]),
    t: float = 0.0
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
    
    self.dims: TubeDims = TubeDims(inner_radius=inner_radius, outer_radius=outer_radius, height=height)
    
    IXX = IYY = self.__m__(t=t) / 12 * (3 * (self.dims.inner_radius ** 2 + self.dims.outer_radius ** 2) + self.dims.height ** 2)
    IZZ = self.__m__(t=t) / 2 * (self.dims.inner_radius ** 2 + self.dims.outer_radius ** 2)
    self.I = array([
      [IXX, 0, 0],
      [0, IYY, 0],
      [0, 0, IZZ]
    ], dtype=float)
    
    self.__seti__(t=t)
  
  def get_i(self, t):
    m = self.__m__(t=t)
    IXX = IYY = m / 12 * (3 * (self.dims.inner_radius ** 2 + self.dims.outer_radius ** 2) + self.dims.height ** 2)
    IZZ = m / 2 * (self.dims.inner_radius ** 2 + self.dims.outer_radius ** 2)
    return array([
      [IXX, 0, 0],
      [0, IYY, 0],
      [0, 0, IZZ]
    ], dtype=float)
  
  def __str__(self) -> str:
    return f"Tube"


class TubeDims(NamedTuple):
  inner_radius: float
  outer_radius: float
  height: float