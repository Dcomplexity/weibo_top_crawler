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