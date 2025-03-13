from typing import Tuple, TypedDict, Type, Dict, List
import pandas as pd
from pandas import DataFrame
from numpy.random import randn as normal_random_variable
import os
import json

DATA_FOLDER = "./Motors/Data/"
AVAILABLE = [name[0] for name in [[file.split(".")[0] for file in files if len(files) > 0 and file.endswith("json")] for _, _, files in os.walk(DATA_FOLDER)] if len(name) > 0]

def getMotorData(motor: str) -> Tuple[DataFrame, Dict[str, List[int]]]:
  motor_csv = "Estes" + motor + ".csv"
  motor_json = motor + ".json"
  
  for _dir, _, _files in os.walk(DATA_FOLDER):
    if motor_csv in _files:
      return (pd.read_csv(_dir + "/" + motor_csv), json.load(open(_dir + "/" + motor_json)))

def getLinearInterpolations(data: DataFrame) -> Tuple[List[float], List[float], List[float]]:
  """ a function to compute the elements required to approximate thrust as a function of time based on a preset motor type
  
  - Usage: Thrust(time) = Thrust_intercept + slope(time) * (time - time_intercept)

  Args:
      data (DataFrame): the loaded csv data into a pandas dataframe

  Returns:
      Tuple[List[float], List[float], List[float]]: slopes, time_intercepts, and the thrust_intercepts
  """
  m = []
  t = []
  thrust = []
  for index in range(len(data) - 1):
    m = (data["Thrust (N)"][index + 1] - data["Thrust (N)"][index]) / (data["Time (s)"][index + 1] - data["Time (s)"][index])
    t = data["Time (s)"][index + 1]
    thrust = data["Thrust (N)"][index]
    
    m.append(m)
    t.append(t)
    thrust.append(thrust)
  
  return (m, t, thrust)

class Motor:
  def __init__(self, motor: str):
    self.motor = motor if motor in AVAILABLE else None
    self.init()
  
  def init(self):
    self.data_frame, self.params = getMotorData(motor=self.motor)
    self.slopes, self.time_intercepts, self.thrust_intercepts = getLinearInterpolations(data=self.data_frame)
    self.burn_time = self.data_frame["Time (s)"][len(self.data_frame["Time (s)"]) - 1]
  
  def thrust(self, t: float) -> float:
    """ computes the scalar thrust of the motor at time t

    Args:
        t (float): time in seconds

    Returns:
        float: thrust in Newtons
    """
    if t < self.burn_time:
      for index, _t in enumerate(self.time_intercepts):
        if t <= _t and t >= 0:
          T = self.thrust_intercepts[index] + self.slopes[index] * (t - self.time_intercepts[index - 1])
          return T if T >= 0 else 0.0
        else:
          pass
    else:
      return 0.0