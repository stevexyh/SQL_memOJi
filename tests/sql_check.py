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


def copy_db(db: pymysql.Connect, new_db_name:str):
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
    print(tables)

    # Copy and insert data
    try:
        for tb in tables:
            new_table = f"""create table {tb} like {db_name}.{tb};"""
            insert_data = f"""insert into {tb} select * from {db_name}.{tb};"""
            new_cur.execute(new_table)
            print(new_table)

            new_cur.execute(insert_data)
            print(insert_data)
            new_db.commit()
    except Exception as exc:
        db.rollback()
        print(exc)

    return tables


# TODO(Steve X): grant privilege on new_db for ojtest user
def deepcopy_db(db_name: str):
    '''Copy database, tables and data'''
    # cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

    db = pymysql.Connect(host='localhost', user='oj', passwd='ojtest+1S', db=db_name)
    new_db_name = db_name+'_copy'

    copy_db(db=db, new_db_name=new_db_name)
    new_db = pymysql.Connect(host='localhost', user='oj', passwd='ojtest+1S', db=new_db_name)
    copy_tables(db=db, new_db=new_db)


if __name__ == "__main__":
    deepcopy_db(db_name='pymysql_test')
