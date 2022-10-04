import pymysql,datetime
host = "127.0.0.1"
port = 3306
user = "root"
passwd = "4b4f8a297c377df7"
db = pymysql.Connect(host=host, port=port, user=user, passwd=passwd)
cur = db.cursor()
cur.execute(f'''show databases;''')
print(cur.fetchall())
cur.execute(f'''use qset_student3;''')
print(cur.fetchall())
# cur.execute(f'''show tables;''')
# tables = [tb[0] for tb in cur.fetchall()]