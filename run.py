import asyncio
from pip import main
from pyppeteer import launch
from pyquery import PyQuery as pq
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Date, Time
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Table
from sqlalchemy.schema import DropTable
from sqlalchemy import MetaData
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
    # print(now_date, now_time)
    # print(records)
    # return now_date, now_time, records
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    global class_name
    data_len = len(records)
    for i in range(data_len):
        # print(type(records[i]))
        data_inst= class_name(top_date=now_date, top_time=now_time, top_rank=records[i][0], keywords=records[i][1], category=records[i][2], top_index=records[i][3], top_remark=records[i][4])
        session.add(data_inst)
    session.commit()
    session.close()


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

def generate_database_url(sql_param):
    sql_url = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(*sql_param)
    return sql_url

async def generate_class():
    global engine
    # global table_name
    tonow = datetime.datetime.now()
    year_num = tonow.year
    month_num = tonow.month
    table_name = "weibo_top_{}_{}".format(year_num, month_num)
    print(table_name)
    base = declarative_base()
    base.metadata.reflect(engine)
    
    # drop table if exists
    try:
        table = base.metadata.tables[table_name]
        base.metadata.drop_all(engine, [table], checkfirst=True)
    except:
        pass

    # create the table
    base = declarative_base()
    base.metadata.reflect(engine)
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
    target_table = Table(table_name, base.metadata, *table_columns_list)
    base.metadata.create_all(engine)

    # create class
    global class_name
    class class_name(base):
        __table__ = Table(table_name, base.metadata, autoload=True)


async def store_data():
    now_date, now_time, records = asyncio.get_event_loop().run_until_complete(weibo_top_crawler())
    data_len = len(records)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    global class_name
    for i in range(data_len):
        data_inst= class_name(top_date=now_date, top_time=now_time, top_rank=records[i][0], keywords=records[i][1], category=records[i][2], top_index=records[i][3], top_remark=records[i][4])
        session.add(data_inst)
    session.commit()
    session.close()

if __name__ == "__main__":
    sql_param = ['dc', 'dc199082', 'localhost', '3306', 'spiders']
    database_url = generate_database_url(sql_param)
    engine = create_engine(database_url)
    table_name = "weibo_top_2022_7"
    print(table_name)
    base = declarative_base()
    base.metadata.reflect(engine)
    class class_name(base):
        __table__ = Table(table_name, base.metadata, autoload=True)    
    # class_name = ""
    # generate_class()
    # store_data()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(generate_class, 'cron', day='1', hour='0', minute='0', second='5')
    # scheduler.add_job(generate_class, 'cron', second=5)
    scheduler.add_job(weibo_top_crawler, 'cron', second='30')
    scheduler.start()
    asyncio.get_event_loop().run_forever()