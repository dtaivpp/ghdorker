from GHDorker import helpers
from GHDorker.dorker import get_client
from datetime import datetime

def test_Limit_step():
  limit = helpers.Limit(
    limit=30,
    remaining=25,
    reset=datetime.now().timestamp() + 10,
    used=5,
    resource="Search")

  limit.step()
  # After stepping a limit the remaining should go down one
  #    and the used should go up one.
  assert limit.remaining == 24 and limit.used == 6


def test_RateLimiter():
  client = get_client()

  rl = helpers.RateLimiter(client=client)
  att_list = [att for att in dir(rl) if isinstance(getattr(rl, att), helpers.Limit) ]

  # There should be more than one Limit attribute on the RateLimiter class
  assert len(att_list) > 1
