from pyppeteer_func import *
from sql_func import *

def build_table(engine, base):
    tonow = datetime.datetime.now()
    year_num = tonow.year
    month_num = tonow.month
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
    return table_name

if __name__ == "__main__":
    # now_date, now_time, total_num, top_rank, keywords, cate_index, top_remark = asyncio.get_event_loop().run_until_complete(weibo_top_crawler())
    # records = manage_data(total_num, top_rank, keywords, cate_index, top_remark)
    sql_url = build_database_url('dc', 'dc199082', 'localhost', '3306', 'spiders')
    engine = create_engine(sql_url)
    base = declarative_base()
    # drop_table('teachers', engine, base)
    # teacher_columns_list =  [
    #     Column('id', Integer, primary_key=True),
    #     Column('firstname', String(14)),
    #     Column('lastname', String(14)),
    #     Column('salary', Integer)]
    # create_table('teachers', teacher_columns_list, engine)

    # Teacher = bind_table('teachers', engine, base)
    # teacher1 = Teacher(id=1, firstname="Mingyang", lastname='Zhang', salary=1000)
    # DBSession = sessionmaker(bind=engine)
    # session = DBSession()
    # session.add(teacher1)
    # session.commit()
    # session.close()
    
    table_name = build_table(engine, base)
