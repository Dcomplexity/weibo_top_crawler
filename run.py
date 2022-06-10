from pyppeteer_test import *

if __name__ == "__main__":
    total_num, top_rank, keywords, cate_index, top_remark = asyncio.get_event_loop().run_until_complete(weibo_top_crawler())
    records = manage_data(total_num, top_rank, keywords, cate_index, top_remark)
    print(records)