import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

async def weibo_top_crawler():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://s.weibo.com/top/summary?cate=realtimehot')
    await page.waitForSelector('.data')
    doc = pq(await page.content())
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
    return total_num, top_rank, keywords, cate_index, top_remark

total_num, top_rank, keywords, cate_index, top_remark = asyncio.get_event_loop().run_until_complete(weibo_top_crawler())

def manage_data(total_num, top_rank, keywords, cate_index, top_remark):
    records = [[] for _ in range(total_num)]
    for i in range(total_num): 
        records[i].append(top_rank[i])
        records[i].append(keywords[i])
        records[i].append(cate_index[i][0])
        records[i].append(cate_index[i][1])
        records[i].append(top_remark[i])
    return records

records = manage_data(total_num, top_rank, keywords, cate_index, top_remark)
print(records)