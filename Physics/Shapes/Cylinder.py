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
    self.I = array([
      [IXX, 0, 0],
      [0, IYY, 0],
      [0, 0, IZZ]
    ], dtype=float)
    
    self.__seti__()
  
  def __str__(self) -> str:
    return f"Cylinder"
  
  def __mass_changed__(self):
    IXX = IYY = self.m * self.dims.height ** 2 / 12 + self.m * self.dims.radius ** 2 / 4
    IZZ = self.m * self.dims.radius ** 2 / 2
    self.I = array([
      [IXX, 0, 0],
      [0, IYY, 0],
      [0, 0, IZZ]
    ], dtype=float)


class CylinderDims(NamedTuple):
  radius: float
  height: float

if __name__ == "__main__":
  s0 = Cylinder(
    1, 1, 5, 1, 1, 1, array([0, 0, 2], float), array([0, 0, 0], float), Quaternion(), array([0, 0, 0], float)
  )
  
  s1 = Cylinder(
    1, 1, 1, 1, 1, 1, array([0, 0, 1], float), array([0, 0, 0], float), Quaternion(), array([0, 0, 0], float)
  )
  
  s2 = Cylinder(
    1, 1, 1, 1, 1, 1, array([0, 0, 0], float), array([0, 0, 0], float), Quaternion(), array([0, 0, 0], float)
  )
  
  s3 = Cylinder(
    1, 1, 1, 1, 1, 1, array([0, 0, -1], float), array([0, 0, 0], float), Quaternion(), array([0, 0, 0], float)
  )
  
  s4 = Cylinder(
    1, 1, 1, 1, 1, 1, array([0, 0, -2], float), array([0, 0, 0], float), Quaternion(), array([0, 0, 0], float)
  )
  
  s: ndarray = s0 + s1 + s2 + s3 + s4
  CM = cm([s0, s1, s2, s3, s4])
  print(s)
  print(CM)
  
  s0.__seti__(CM)
  s1.__seti__(CM)
  s2.__seti__(CM)
  s3.__seti__(CM)
  s4.__seti__(CM)
  
  s: ndarray = s0 + s1 + s2 + s3 + s4
  print(s)