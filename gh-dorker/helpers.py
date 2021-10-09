from datetime import datetime
from time import sleep
from pprint import pprint

class Limits():
  def __init__(self, limit, remaining, reset, used, resource):  
    self.limit = limit
    self.remaining = remaining
    self.reset = reset
    self.used = used
    self.resource = resource
  
  def step(self):
    self.remaining = self.remaining -1
    self.used = self.used + 1

  def __str__(self):
    return f"""\n
            limit: {self.limit} 
            remaining: {self.remaining}
            reset: {self.reset}
            used: {self.used}
            resource: {self.resource}"""

class RateLimiter:
  def __init__(self, client):
    self.client = client
    self.initialize_limits()
  
  def initialize_limits(self):
    limits = self.client.rate_limit.get()
    #pprint(limits)
    for key, value in limits["resources"].items():
      #print(f"{key}, {value}")
      setattr(self, key, Limits(**value, resource=key))

  def check_safety(self, endpoint):
    rate_limit = getattr(self, endpoint)
    curr_time = datetime.now().timestamp()
    
    #if rate_limit.used < rate_limit.limit-1:
    #  rate_limit.step()
    #  return
    
    if curr_time < rate_limit.reset:
      sleep(((rate_limit.reset - curr_time) / rate_limit.remaining)+1)
    else: 
      self.initialize_limits()

    rate_limit.step()
    return


#def rate_limiter(func, endpoint: str):
#  if rate_limits == None:
#    rate_limits = RateLimiter(get_client())
#
#  rate_limits.check_safety()
#  @functools.wraps(func)
#  def wrapper(*args, **kwargs):
#    return func(*args, **kwargs)
#
#  return wrapper