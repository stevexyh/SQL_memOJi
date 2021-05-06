#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : sql_run.py
* Description  : run SQL for questions
* Create Time  : 2021-05-06 16:21:47
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh/SQL_memOJi
----------------------------------------------------------------------------------------------------
* Notice
- 
- 
----------------------------------------------------------------------------------------------------
'''


import pymysql
import beeprint


# 打开数据库连接
db = pymysql.Connect(host="localhost", user="oj", passwd="ojtest+1S", db="pymysql_test")

# 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)



# # SQL 插入语句
# sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
#     LAST_NAME, AGE, SEX, INCOME) \
#     VALUES (%s, %s, %s, %s, %s)"
#     # VALUES ('wtf', 'Mohan', 20, 'M', 2000)"

# val = (
#     ('????', 'Mohan', 20, 'M', 2000),
#     ('1Mac', 'Mohan', 20, 'M', 2000),
#     ('2Mac', 'Mohan', 20, 'M', 2000),
#     ('3Mac', 'Mohan', '20', 'M', 2000),
# )


# try:
#     # cursor.executemany(sql,val)
#     sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
#         LAST_NAME, AGE, SEX, INCOME) \
#         VALUES ('wtf', 'Mohan', '20aaa', 'M', 2000)"
#     # drop 之前的 sql 会被自动 commit
#     cursor.execute("""drop table employee""")
#     cursor.execute(sql)
#     # cursor.execute(sql)
# except Exception as err:
#     db.rollback()
#     print(err)

# cursor.execute("""select * from employee""")
# # cursor.execute("""show create table employee;""")
# data = cursor.fetchone()
# beeprint.pp(data)
# print(cursor.rowcount)
# print(cursor.rownumber)
# # db.rollback()
# # 关闭数据库连接
# cursor.close()
# db.close()

if __name__ == "__main__":
    pass
