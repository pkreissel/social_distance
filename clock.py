from apscheduler.schedulers.blocking import BlockingScheduler
from places import api_call

sched = BlockingScheduler()

#@sched.scheduled_job('cron', day_of_week='*', hour='9-21/1', misfire_grace_time=1000)
@sched.scheduled_job('cron', hour='9-18/3', misfire_grace_time=1000)
def timed_job():
    print('This job is run everyday every 3 hours from 6-18h')
    api_call()

sched.start()
