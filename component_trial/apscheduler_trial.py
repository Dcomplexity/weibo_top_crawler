import asyncio
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import os

def job_1():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def job_2():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Hello")

async def tick_1():
    print("Tick! The time is %s" %datetime.now())

async def tick_2():
    print("Hello you, Notice the time is %s" %datetime.now())

# BlockingScheduler

# scheduler = BlockingScheduler()
# scheduler.add_job(job_1, 'cron', minute='0-59', second='*/5')
# scheduler.add_job(job_2, "cron", minute='0-59', second='*/5')
# scheduler.start()

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(tick_1, 'interval', seconds=3)
    scheduler.add_job(tick_2, 'interval', seconds=5)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    asyncio.get_event_loop().run_forever()