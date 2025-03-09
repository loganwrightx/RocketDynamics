from __future__ import annotations
from typing import overload
from numpy import ndarray, sin, cos, array, dot, cross, exp
from numpy.linalg import norm

W, I, J, K = 0, 1, 2, 3

class Quaternion:
  w: float
  x: float
  y: float
  z: float
  
  @overload
  def __init__(self): ...
  
  @overload
  def __init__(self, angle: float | int, axis: list | ndarray[float]): ...
  
  @overload
  def __init__(self, w: float | int, x: float | int, y: float | int, z: float | int): ...
  
  def __init__(self, *args):
    if len(args) == 0:
      self.w = 1.0
      self.x = 0.0
      self.y = 0.0
      self.z = 0.0
    
    elif len(args) == 2:
      angle = args[0]
      axis = args[1]
      if isinstance(angle, (float, int)) and isinstance(axis, (list, ndarray)):
        _is3d(axis)
        self.w = cos(angle / 2)
        self.x = axis[0] * sin(angle / 2)
        self.y = axis[1] * sin(angle / 2)
        self.z = axis[2] * sin(angle / 2)
      else:
        raise TypeError("Cannot create a Quaternion() object, invalid angle and vector passed to constructor!")
    
    elif len(args) == 4:
      w, x, y, z = args
      self.w = w
      self.x = x
      self.y = y
      self.z = z
    
    else:
      raise NotImplemented("Invalid constructor call for Quaternion obj!")
  
  def norm(self) -> None:
    norm = self.mag()
    if norm > 0.0:
      self.w /= norm
      self.x /= norm
      self.y /= norm
      self.z /= norm
    else:
      self.w = 1.0
      self.x = 0.0
      self.y = 0.0
      self.z = 0.0
  
  def mag(self) -> float:
    return (self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z) ** 0.5
  
  def conj(self) -> Quaternion:
    return Quaternion(self.w, - self.x, - self.y, - self.z)
  
  def vec_part(self) -> ndarray:
    return array([self.x, self.y, self.z], float)
  
  def rot_mat(self) -> ndarray:
    _identity = array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], float)
    _skew_symmetric = array([
      [0, -self.z, self.y],
      [self.z, 0, -self.x],
      [-self.y, self.x, 0]
    ], dtype=float)
    return _identity + 2 * self.w * _skew_symmetric + 2 * _skew_symmetric @ _skew_symmetric
  
  def copy(self) -> Quaternion:
    return Quaternion(self[W], self[I], self[J], self[K])
  
  def __str__(self):
    return f"q = ({self.w:.4f} {self.x:.4f}i {self.y:.4f}j {self.z:.4f}k)"
  
  def __mul__(self, other: float | int | Quaternion):
    if isinstance(other, (float, int)):
      return Quaternion(self.w * other, self.x * other, self.y * other, self.z * other)
    elif isinstance(other, Quaternion):
      return _hamiltonProduct(self, other)
    else:
      return NotImplemented
  
  def __rmul__(self, other: int | float | Quaternion):
    if isinstance(other, (float, int)):
      return self.__mul__(other)
    elif isinstance(other, Quaternion):
      return _hamiltonProduct(other, self)
    else:
      return NotImplemented
  
  def __getitem__(self, key: int):
    match key:
      case 0:
        return self.w
      case 1:
        return self.x
      case 2:
        return self.y
      case 3:
        return self.z
      case _:
        raise IndexError("Quaternion only has indeces 0 through 3 (4 elements total)!")

def _hamiltonProduct(q1: Quaternion, q2: Quaternion) -> Quaternion:
  q1_v = q1.vec_part()
  q2_v = q2.vec_part()
  w = q1[W] * q2[W] - dot(q1_v, q2_v)
  v = q1[W] * q2_v + q2[W] * q1_v + cross(q1_v, q2_v)
  return Quaternion(w, v[0], v[1], v[2])

def qexp(q: Quaternion) -> Quaternion:
  w: float = q[W]
  v : ndarray = q.vec_part()
  theta: float = q.mag()
  return exp(w) * Quaternion(theta, v)

def vrot(q: Quaternion, v: ndarray):
  _is3d(v)
  q_v = v2q(v)
  q.norm()
  q_inv = q.conj()
  return (q * q_v * q_inv).vec_part()

def v2q(v: ndarray) -> Quaternion:
  _is3d(v)
  return Quaternion(0.0, v[0], v[1], v[2])

def _is3d(v: ndarray):
  if len(v) == 3:
    return None
  else:
    raise AttributeError("Vector is not length 3!")

__all__ = [
  "Quaternion",
  "I",
  "J",
  "K",
  "qexp",
  "vrot",
  "v2q"
]

if __name__ == "__main__":
  q1 = Quaternion(3.14159 / 2, array([1, 0, 0]))
  q1.norm()
  
  q2 = Quaternion(3.14159 / 2, array([0, 0, 1]))
  q2.norm()
  
  q3 = Quaternion(3.14159 / 2, array([0, 1, 0]))
  q3.norm()
  
  v = array([0.0, 0.0, 1.0])
  
  v = vrot(q1, v)
  print(v)
  
  v = vrot(q2, v)
  print(v)
  
  v = vrot(q3, v)
  print(v)