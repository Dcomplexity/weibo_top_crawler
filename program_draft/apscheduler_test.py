import asyncio
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import os

def job_1():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def job_2():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Hello")

async def tick():
    print("Tick! The time is %s" %datetime.now())

# BlockingScheduler

# scheduler = BlockingScheduler()
# scheduler.add_job(job_1, 'cron', minute='0-59', second='*/5')
# scheduler.add_job(job_2, "cron", minute='0-59', second='*/5')
# scheduler.start()

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    asyncio.get_event_loop().run_forever()