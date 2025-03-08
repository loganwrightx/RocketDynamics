from __future__ import annotations
from typing import Tuple, overload
from numpy import ndarray

from Quaternion import *

def dq(omega: ndarray, alpha: ndarray, dt: float) -> Tuple[Quaternion, ndarray]:
  """ attitude differentials

  Args:
      omega (ndarray): angular velocity
      alpha (ndarray): angular acceleration
      dt (float): small time step

  Returns:
      Tuple[Quaternion, ndarray]: change in attitude, change in angular velocity
  """
  return qexp(v2q(omega * dt)), alpha * dt

def dr(vel: ndarray, acc: ndarray, dt: float) -> Tuple[ndarray, ndarray]:
  """ linear position differentials

  Args:
      vel (ndarray): linear velocity
      acc (ndarray): linear acceleration
      dt (float): small time step

  Returns:
      Tuple[ndarray, ndarray]: change in linear position, change in linear velocity
  """
  return vel * dt, acc * dt

