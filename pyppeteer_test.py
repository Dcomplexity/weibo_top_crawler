import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

async def weibo_top_crawler():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://s.weibo.com/top/summary?cate=realtimehot')
    await page.waitForSelector('.data')
    doc = pq(await page.content())
    names = [item.text() for item in doc('.td-01').items()]
    print(names)
    for key in names:
        # if key != '':
        try:
            print(int(key))
        except:
            print('wrong')
    print('Names: ', names)
    await browser.close()

asyncio.get_event_loop().run_until_complete(weibo_top_crawler())

