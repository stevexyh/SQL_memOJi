#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : sql_check.py
* Description  : check the correctness for each SQL
* Create Time  : 2021-05-06 16:22:23
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
from utils import token as tk


def clear_db(cur: pymysql.Connect.cursor, db_name: str):
    '''Clear database'''

    cur.execute(f"""DROP DATABASE IF EXISTS {db_name}""")


def copy_db(db: pymysql.Connect, new_db_name: str):
    '''Copy only database'''

    cur = db.cursor()
    db_name = db.db.decode()

    # Show SQL of create db
    cur.execute(f"""show create database {db_name}""")
    res = cur.fetchone()[1]

    # Create db
    try:
        clear_db(cur=cur, db_name=new_db_name)
        db_new_sql = res.replace(db_name, new_db_name).replace('CREATE DATABASE', 'CREATE DATABASE IF NOT EXISTS')
        cur.execute(db_new_sql)
        db.commit()
    except Exception as exc:
        db.rollback()
        print('copy_db:', exc)


def copy_tables(db: pymysql.Connect, new_db: pymysql.Connect):
    '''Copy all tables and data'''

    db_name = db.db.decode()
    cur = db.cursor()
    new_cur = new_db.cursor()

    cur.execute("""show tables;""")
    tables = [tb[0] for tb in cur.fetchall()]

    # Copy and insert data
    try:
        for tb in tables:
            new_table = f"""create table {tb} like {db_name}.{tb};"""
            insert_data = f"""insert into {tb} select * from {db_name}.{tb};"""
            new_cur.execute(new_table)
            new_cur.execute(insert_data)

            new_db.commit()
    except Exception as exc:
        db.rollback()
        print('copy_tables', exc)

    return tables


# TODO(Steve X): grant privilege on new_db for ojtest user
def deepcopy_db(db_name: str, new_db_name: str):
    '''Copy database, tables and data'''
    # cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

    tmp_user = tk.get_conf('mysql', 'temp_user')
    tmp_passwd = tk.get_conf('mysql', 'temp_user_password')

    root_host = tk.get_conf('mysql', 'host')
    root_port = int(tk.get_conf('mysql', 'port'))
    root_user = tk.get_conf('mysql', 'user')
    root_passwd = tk.get_conf('mysql', 'password')

    root_db = pymysql.Connect(host=root_host, port=root_port, user=root_user, passwd=root_passwd, db=db_name)
    root_cur = root_db.cursor()
    # print(f'''GRANT SELECT ON {db_name}.* to '{tmp_user}';''')
    root_cur.execute(f'''GRANT SELECT ON {db_name}.* to '{tmp_user}';''')
    root_cur.execute(f'''GRANT ALL ON {new_db_name}.* to '{tmp_user}';''')

    copy_db(db=root_db, new_db_name=new_db_name)
    tmp_new_db = pymysql.Connect(host=root_host, user=tmp_user, passwd=tmp_passwd, db=new_db_name)
    copy_tables(db=root_db, new_db=tmp_new_db)

    root_cur.close()
    root_db.close()

    return tmp_new_db.cursor()


def diff(cur_1: pymysql.Connect.cursor, cur_2: pymysql.Connect.cursor):
    '''Check if two databases are identical'''
    # Seddon has seen
    cur_1.execute("""show tables;""")
    tables = [tb[0] for tb in cur_1.fetchall()]
    res = True

    # TODO(Steve X): 检验索引、视图
    for tb in tables:
        cur_1.execute(f"""select * from {tb};""")
        cur_2.execute(f"""select * from {tb};""")
        res_1 = cur_1.fetchall()
        res_2 = cur_2.fetchall()
        # XXX:此处可以查看每张表是否一致
        # TODO:尝试可以加入日志功能 方便用户更快知道自己错在哪了
        # print(tb, res_1 == res_2)
        res &= res_1 == res_2

    return res


def ans_check(db_nm: str, ans_sql: str, stud_sql: str) -> bool:
    '''
    Check the correctness of SQL from students

    Parameters::
        ans_sql: str - standard answer
        stud_sql: str - SQL from students
    Returns::
        res: bool - if the SQL is correct
    '''
    print("判断执行结果.....")
    new_db_nm = db_nm+'_copy'
    new_db_name_1 = new_db_nm+'1'
    new_db_name_2 = new_db_nm+'2'
    #Copy the Database
    cur_1 = deepcopy_db(db_name=db_nm, new_db_name=new_db_name_1)
    cur_2 = deepcopy_db(db_name=db_nm, new_db_name=new_db_name_2)
    print("双数据库拷贝成功")
    cur_1.execute(ans_sql)
    cur_2.execute(stud_sql)
    res_1 = cur_1.fetchall()
    res_2 = cur_2.fetchall()
    exe_diff = res_1 == res_2
    data_diff = diff(cur_1=cur_1,cur_2=cur_2)
    print("Execute identify",exe_diff)
    #XXX 可以在前端提示是数据不一致还是返回结果不一致
    print(res_1)
    print("----------------------------")
    print(res_2)
    print("Data identify:",data_diff)
    res = (exe_diff) and data_diff
    clear_db(cur=cur_1, db_name=new_db_name_1)
    clear_db(cur=cur_2, db_name=new_db_name_2)
    cur_1.close()
    cur_2.close()

    return res


# XXX(Steve X): cursor.close(), connection.close()
if __name__ == "__main__":
    crct = ans_check(ans_sql='select * from employee;', stud_sql='select SEX from employee;')
    print(crct)
