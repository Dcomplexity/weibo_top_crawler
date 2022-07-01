from pyppeteer_func import *
from sql_func import *
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import *

def build_table(engine, base):
    tonow = datetime.datetime.now()
    year_num = tonow.year
    month_num = tonow.month
    global table_name
    table_name = "weibo_top_{}_{}".format(year_num, month_num)
    drop_table(table_name, engine, base) 
    table_columns_list = [
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('top_date', Date),
        Column('top_time', Time),
        Column('top_rank', String(5)),
        Column('keywords', String(127)),
        Column('category', String(10)),
        Column('top_index', String(127)),
        Column('top_remark', String(5)),
    ]
    create_table(table_name, table_columns_list, engine)
    global data_class
    data_class = bind_table(table_name, engine, base)

# async def get_store_data():
#     now_date, now_time, total_num, top_rank, keywords, cate_index, top_remark = asyncio.get_event_loop().run_until_complete(weibo_top_crawler())
#     records = manage_data(total_num, top_rank, keywords, cate_index, top_remark)
#     data_len = len(records)
#     session = DBSession()
#     for i in range(data_len):
#         data_inst = data_class(top_date=now_date, top_time=now_time, top_rank=records[i][0], keywords=records[i][1], category=records[i][2], top_index=records[i][3], top_remark=records[i][4])
#         session.add(data_inst)
#     session.commit()
#     session.close()


if __name__ == "__main__":
    sql_url = build_database_url('dc', 'dc199082', 'localhost', '3306', 'spiders')
    engine = create_engine(sql_url)
    base = declarative_base()
    print(base)
    base.metadata.reflect(engine)
    tables = base.metadata.tables
    print(tables)
    # table_name = "weibo_top_2022_6"
    # data_class = ""

    # scheduler = AsyncIOScheduler()
    # scheduler.add_job(build_table, 'cron', day='1', hour='0', minute='0', second='5', args=[engine, base])
    # scheduler.add_job(weibo_top_crawler, 'cron', second='30')
    # # scheduler = BlockingScheduler()
    # # scheduler.add_job(build_table, 'cron', day='1', hour='0', minute='0', second='5', args=[engine, base])
    # # scheduler.add_job(weibo_top_crawler, 'cron', second='30')
    # scheduler.start()
    # asyncio.get_event_loop().run_forever()