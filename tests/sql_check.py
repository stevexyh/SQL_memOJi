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
# import beeprint


# try:
#     cursor.execute(sql)
#     db.commit()
# except:
#     db.rollback()

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
        print(exc)


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
        print(exc)

    return tables


# TODO(Steve X): grant privilege on new_db for ojtest user
def deepcopy_db(db_name: str, new_db_name: str):
    '''Copy database, tables and data'''
    # cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

    db = pymysql.Connect(host='localhost', user='oj', passwd='ojtest+1S', db=db_name)

    copy_db(db=db, new_db_name=new_db_name)
    new_db = pymysql.Connect(host='localhost', user='oj', passwd='ojtest+1S', db=new_db_name)
    copy_tables(db=db, new_db=new_db)
    db.close()

    return new_db.cursor()


def diff(cur_1: pymysql.Connect.cursor, cur_2: pymysql.Connect.cursor):
    '''Check if two databases are identical'''

    cur_1.execute("""show tables;""")
    tables = [tb[0] for tb in cur_1.fetchall()]
    res = True

    for tb in tables:
        cur_1.execute(f"""select * from {tb};""")
        cur_2.execute(f"""select * from {tb};""")
        res_1 = cur_1.fetchall()
        res_2 = cur_2.fetchall()

        print(tb, res_1 == res_2)
        res &= res_1 == res_2

    return res


def ans_check(ans_sql: str, stud_sql: str) -> bool:
    '''
    Check the correctness of SQL from students

    Parameters::
        ans_sql: str - standard answer
        stud_sql: str - SQL from students
    Returns::
        res: bool - if the SQL is correct
    '''

    db_nm = 'pymysql_test'
    new_db_nm = db_nm+'_copy'
    new_db_name_1 = new_db_nm+'1'
    new_db_name_2 = new_db_nm+'2'

    cur_1 = deepcopy_db(db_name=db_nm, new_db_name=new_db_name_1)
    cur_2 = deepcopy_db(db_name=db_nm, new_db_name=new_db_name_2)

    cur_1.execute(ans_sql)
    cur_2.execute(stud_sql)
    res_1 = cur_1.fetchall()
    res_2 = cur_2.fetchall()

    res = (res_1 == res_2) and diff(cur_1=cur_1, cur_2=cur_2)
    clear_db(cur=cur_1, db_name=new_db_name_1)
    clear_db(cur=cur_2, db_name=new_db_name_2)
    cur_1.close()
    cur_2.close()

    return res


# XXX(Steve X): cursor.close(), connection.close()
if __name__ == "__main__":
    crct = ans_check(ans_sql='select * from employee;', stud_sql='select SEX from employee;')
    print(crct)
