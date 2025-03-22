from __future__ import annotations

class PID:
  ie: float = 0.0
  e: float = 0.0
  de: float = 0.0
  
  t_last: float = 0.0
  
  def __init__(self, pid: tuple[float, float, float], compute_freuency: int, setpoint: float, lag_steps: int, t: float):
    self.kp, self.ki, self.kd = pid
    self.freq = compute_freuency
    self.period = 1 / compute_freuency
    self.setpoint = setpoint
    self.lag = lag_steps
    self.t_last = t
  
  def step(self, t: float, value: float) -> float | None:
    if (t - self.t_last) >= self.period:
      dt = t - self.t_last
      e_old = self.e
      e_new = (self.setpoint - value)
      
      self.ie += (e_new + e_old) / 2 * dt
      self.e = e_new
      self.de = (e_new - e_old) / dt
      
      self.t_last = t
      
      return self.kp * self.e + self.ki * self.ie + self.kd * self.de
    
    return None
  
  def update_setpoint(self, setpoint: float) -> None:
    self.setpoint = setpoint
    