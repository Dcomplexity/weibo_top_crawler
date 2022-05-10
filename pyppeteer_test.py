import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://s.weibo.com/top/summary?cate=realtimehot')
    await page.waitForSelector('.data')
    doc = pq(await page.content())
    names = [item.text() for item in doc('.td-02').items()]
    print('Names: ', names)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

