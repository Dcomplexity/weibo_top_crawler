from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Date, Time
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Table
from sqlalchemy.schema import DropTable
from sqlalchemy import MetaData
import datetime

def generate_database_url(sql_param):
    sql_url = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(*sql_param)
    return sql_url

def generate_class():
    global engine
    # global table_name
    tonow = datetime.datetime.now()
    year_num = tonow.year
    month_num = tonow.month
    table_name = "weibo_top_2022_6"
    # table_name = "weibo_top_{}_{}".format(year_num, month_num)
    base = declarative_base()
    base.metadata.reflect(engine)
    
    # drop table if exists
    try:
        table = base.metadata.tables[table_name]
        base.metadata.drop_all(engine, [table], checkfirst=True)
    except:
        pass

    # create the table
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


if __name__ == "__main__":
    sql_param = ['dc', 'dc199082', 'localhost', '3306', 'spiders']
    database_url = generate_database_url(sql_param)
    engine = create_engine(database_url)
    class_name = ""
    generate_class()
    print(class_name)
