from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Date, Time
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Table
from sqlalchemy.schema import DropTable
from sqlalchemy import MetaData

# sql_user_name = 'dc'
# sql_user_password = 'dc199082'
# sql_base_url = 'localhost'
# sql_base_port = '3306'
# sql_schema_name = 'spider'
# sql_param = [sql_user_name, sql_user_password, sql_base_url, sql_base_port, sql_schema_name]
# sql_url = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(*sql_param)
# engine = create_engine(sql_url)
# Base = declarative_base()

def build_database_url(sql_user_name, sql_user_password, sql_base_url, sql_base_port, sql_schema_name):
    sql_param = [sql_user_name, sql_user_password, sql_base_url, sql_base_port, sql_schema_name]
    sql_url = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(*sql_param)
    return sql_url

def drop_table(table_name, engine, base):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    try:
        table = metadata.tables[table_name]
        base.metadata.drop_all(engine, [table], checkfirst=True)
    except:
        pass


def create_table(table_name, table_columns, engine):
    metadata = MetaData()
    target_table = Table(
        table_name, metadata,
        *table_columns
    )
    metadata.create_all(engine)


def bind_table(table_name, engine, base):
    metadata = base.metadata
    metadata.bind = engine
    class class_name(base):
        __table__ = Table(table_name, metadata, autoload=True)
    return class_name