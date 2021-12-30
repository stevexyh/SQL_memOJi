#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : token.py
* Description  : Get token from files
* Create Time  : 2021-04-03 23:34:10
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh/SQL_memOJi
----------------------------------------------------------------------------------------------------
* Notice
- 
- 
----------------------------------------------------------------------------------------------------
'''
# TODO(Steve X): 文件不存在时创建文件

import configparser


TOKEN_FILE = '.sec_key'
INIT_CONF = '.init.conf'

try:
    conf = configparser.ConfigParser()
    conf.read(INIT_CONF)
except FileNotFoundError as err:
    print(err)

    info = f'''
    INFO: Token file {INIT_CONF} missing.
            - Please create file {INIT_CONF} at root dir of the project.
            - Please fill in your config info in the same format of {INIT_CONF}.sample.
            - Maybe you are not permitted to run this project.
    '''

    print(info)


def get_token():
    '''Get token from files'''
    token = ''
    try:
        with open(TOKEN_FILE, 'r') as tk_file:
            token = tk_file.readline().strip()
    except FileNotFoundError as err:
        print(err)

        info_str = f'''
        INFO: Token file {TOKEN_FILE} missing.
                - Please create file {TOKEN_FILE} at root dir of the project.
                - Please fill in your SECRET KEY for the project.
                - Maybe you are not permitted to run this project.
        '''

        print(info_str)

    return token


def get_weather_key():
    '''Get weather api key from files'''
    token = conf.get('weather', 'key')

    return token


def get_conf(section: str = '', option: str = ''):
    '''Get config from files'''
    res = conf.get(section=section, option=option)

    return res
