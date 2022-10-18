import pymysql,datetime
host = "127.0.0.1"
port = 3306
user = "root"
passwd = "4b4f8a297c377df7"
db = pymysql.Connect(host=host, port=port, user=user, passwd=passwd)
cur = db.cursor()
cur.execute(f'''show databases;''')
print(cur.fetchall())
cur.execute(f'''use qset_SPJ_MNG;''')
print(cur.fetchall())
cur.execute(f'''select jname from j where jno in ( select distinct jno from spj where sno in ( select sno from s where city='上海' ) order by jno );''')
a = sorted(cur.fetchall())
# print(sorted(cur.fetchall()))
print(a)
cur.execute(f'''select distinct jname from j where exists(select * from spj,s where spj.jno = j.jno and spj.sno = s.sno and s.city = '上海');''')
# print(sorted(cur.fetchall()))
b = sorted(cur.fetchall())
# print(sorted(cur.fetchall()))
print(b)
print(a == b)
# cur.execute(f'''show tables;''')
# tables = [tb[0] for tb in cur.fetchall()]
# print(tables)