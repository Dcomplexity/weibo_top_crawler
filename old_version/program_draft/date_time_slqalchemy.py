import datetime
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Table
from sqlalchemy.schema import DropTable
from sqlalchemy import MetaData



engine = create_engine('mysql+mysqlconnector://dc:dc199082@localhost:3306/spiders')
Base = declarative_base()
# metadata = Base.metadata
# metadata.bind = engine


def drop_table(table_name, engine=engine):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    try:
        table = metadata.tables[table_name]
        Base.metadata.drop_all(engine, [table], checkfirst=True)
    except:
        pass


def create_table(table_name, table_columns, engine=engine):
    metadata = MetaData()
    target_table = Table(
        table_name, metadata,
        *table_columns
    )
    metadata.create_all(engine)


def bind_table(table_name, engine=engine):
    metadata = Base.metadata
    metadata.bind = engine
    class class_name(Base):
        __table__ = Table(table_name, metadata, autoload=True)
    return class_name


drop_table('teachers')
teacher_columns_list =  [
        Column('id', Integer, primary_key=True),
        Column('name', String(14)),
        Column('lastname', String(14)),
        Column('Salary', Integer)]
create_table('teachers', teacher_columns_list)

Teacher = bind_table('teachers')
teacher1 = Teacher(id=1, name="Chuang", lastname='Deng', Salary=1000)
DBSession = sessionmaker(bind=engine)
session = DBSession()
session.add(teacher1)
session.commit()
session.close()



# target_table = Table(
#     table_name, metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name', String(16)),
#     Column('lastname', String(16)),
#     Column('Salary', Integer),
# )

# metadata.create_all()

# class User():
#     def __init__(self, name):
#         self.name = name
#         tonow = datetime.datetime.now().replace(microsecond=0)
#         self.create_date = tonow.date()
#         self.create_time = tonow.time()
    
#     def get_info(self):
#         return self.name, self.create_date, self.create_time

#     __tablename__ = 'user_test'
#     name = Column()

# class User(Base):
#     __table__ = Table("user_test", metadata, autoload=True)

# DBSession = sessionmaker(bind=engine)
# session = DBSession()
# tonow = datetime.datetime.now().replace(microsecond=0)
# user1 = User(user_name="DC", create_date=tonow.date(), create_time=tonow.time())
# session.add(user1)
# session.commit()
# session.close()
