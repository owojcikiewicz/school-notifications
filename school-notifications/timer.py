import sched, time
import asyncio
from main import main
import config  

s = sched.scheduler(time.time, time.sleep)
def check(sc): 
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    s.enter(config.check_time, 1, check, (sc,))

s.enter(config.check_time, 1, check, (s,))
s.run()