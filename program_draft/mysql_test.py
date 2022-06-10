import pymysql

id = '20120002'
user = 'Bob'
age = 20

db = pymysql.connect(host="localhost", user="dc", password="dc199082", port=3306, db='spiders')
cursor = db.cursor()
cursor.execute('SELECT VERSION()')
data = cursor.fetchone()
print('Database version:', data)
sql = 'INSERT INTO students(id, name, age) values(%s, %s, %s)'
try:
    cursor.execute(sql, (id, user, age))
    db.commit()
except:
    db.rollback()

sql = 'UPDATE students SET age=%s WHERE name = %s'
try:
    cursor.execute(sql, (25, 'Bob'))
    db.commit()
except:
    db.rollback()


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