from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='*', ,hour='9-21/3')
def timed_job():
    print('This job is run everyday every 3 hours from 6-21h')
    subprocess.call('python places.py', shell=True, close_fds=True)

sched.start()
