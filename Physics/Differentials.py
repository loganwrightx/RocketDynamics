from __future__ import annotations
from typing import Tuple
from numpy import ndarray, array

from Shapes.Quaternion import *
from ThrustVectoring.ThrustVector import ThrustVector

def dq(omega: ndarray, dt: float) -> Quaternion:
  """ attitude differentials

  Args:
      omega (ndarray): angular velocity
      dt (float): small time step

  Returns:
      Tuple[Quaternion, ndarray]: change in attitude, change in angular velocity
  """
  return qexp(v2q(omega * dt))

def dr(r: ndarray, dt: float, ) -> ndarray:
  """ linear position differentials

  Args:
      r (ndarray): vector containing position, velocity, angular velocity
      dt (float): small time step

  Returns:
      Tuple[ndarray, ndarray]: change in linear position, change in linear velocity
  """
  acc = array([0.0, 0.0, 0.0])
  alpha = array([0.0, 0.0, 0.0])
  return array([r[1], acc, alpha], dtype=float)

__all__ = [
    "dq",
    "dr"
]