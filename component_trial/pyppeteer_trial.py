import asyncio
from pip import main
from pyppeteer import launch
from pyquery import PyQuery as pq
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime

async def weibo_top_crawler():

    # connect to the web(https://s.weibo.com/top/summary?cate=realtimehot)
    browser = await launch()
    page = await browser.newPage()
    tonow = datetime.datetime.now().replace(microsecond=0)
    now_date = tonow.date()
    now_time = tonow.time()
    await page.goto('https://s.weibo.com/top/summary?cate=realtimehot')
    await page.waitForSelector('.data')
    doc = pq(await page.content())

    # get the data from the web
    top_rank = [item.text() for item in doc('.td-01').items()]
    total_num = len(top_rank)
    for i in range(total_num):
        if top_rank[i] == '':
            top_rank[i] = 'top'
    keywords = [item.text() for item in doc('.td-02 a').items()]
    cate_index = [item.text().split() for item in doc('.td-02 span').items()]
    cate_index.insert(0, ['top', 'top'])
    for item in cate_index:
        if len(item) == 0:
            item.append('')
            item.append('')
        elif len(item) == 1:
            item.insert(0, '') 
    top_remark = [item.text() for item in doc('.td-03').items()]
    await browser.close()

    records = manage_data(total_num, top_rank, keywords, cate_index, top_remark)
    # return records
    print(now_date, now_time)
    print(records)


# manage the data and store it to a list
def manage_data(total_num, top_rank, keywords, cate_index, top_remark):
    records = [[] for _ in range(total_num)]
    for i in range(total_num): 
        records[i].append(top_rank[i])
        records[i].append(keywords[i])
        records[i].append(cate_index[i][0])
        records[i].append(cate_index[i][1])
        records[i].append(top_remark[i])
    return records


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(weibo_top_crawler, 'interval', seconds=30)
    scheduler.start()
    asyncio.get_event_loop().run_forever()
    # records = asyncio.get_event_loop().run_until_complete(weibo_top_crawler())
    # now_date, now_time, total_num, top_rank, keywords, cate_index, top_remark = weibo_top_crawler()
    # records = manage_data(total_num, top_rank, keywords, cate_index, top_remark)
    # print(records)
    # print(now_date, now_time)