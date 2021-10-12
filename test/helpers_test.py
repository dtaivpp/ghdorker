from GHDorker import helpers
from datetime import datetime

def test_Limits_step():
  limit = helpers.Limits(    
    limit=30,
    remaining=25,
    reset=datetime.now().timestamp() + 10,
    used=5,
    resource="Search")
  
  limit.step()
  # After stepping a limit the remaining should go down one
  #    and the used should go up one. 
  assert limit.remaining == 24 and limit.used == 6

