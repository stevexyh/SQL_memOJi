# Installation Guide For SQL-OJ
## Environment
- Ubuntu 20.04 LTS
- Python 3.8.10
- Mysql MariaDB 10.0(MyISAM)
- Django 3.1.7
- Celery 5.1.2
- Redis 6.2.6
- DjangoRestFramework 3.13.1
- mysqlclient 2.1.0
- PyMySQL 1.0.2
- Prettytable 2.5.0
## Download Code
```shell
git clone https://github.com/SeddonShen/SQL_memOJi.git
cd ./SQL_memOJi/src
```
## Pre Preparation
Mysql，Redis请自行安装相应版本，Redis配置好后还需要在./src/SQL_memOJi/celery.py文件中修改相应Redis broker地址，以及src/SQL_memOJi/settings.py中相应的broker_url和result_backend地址。下述**配置Redis**章节有详细介绍。
安装好Mysql和Redis之后再进行下述步骤。
**注意：Mysql的Engine不能是InnoDB，必须是MyISAM	!**
### 安装依赖
```bash
sudo apt-get install libmysqlclient-dev
pip install django==3.1.7 celery==5.1.2 djangorestframework==3.13.1 mysqlclient==2.1.0 pymysql==1.0.2 prettytable==2.5.0 redis==4.1.3
```
上述版本为推荐版本，可以进行适当的升级操作，具体操作可灵活选择。
## First use 添加配置文件
### Renew or Edit a config file like (/src/.inif.conf.sample) 新建/src/.inif.conf文件
内容如下：
```config
[mysql]
# Django Settings
name = oj
host = 127.0.0.1
port = 3306
# Root User's Username and Password(For Django and OJCheck Use)
user = root
password = 4b4f8a297c377df7
# Temp User's Username and Password(Just for OJCheck Use)
temp_user = oj
temp_user_password = ojtest+1S
```
Pay attention that you need two database account (root and temp account) in the same database.
**You can edit the file(.init.conf.sample) and rename this file as '.init.conf' or make a new file.**
### Token file 新建Token文件
用于密码校验，在src目录下新建.sec_key文件，长度固定，下面的字符串可以做出修改，内容不要和下面的一样。
Like the previous step, new a file named '.sec_key' in the src folder like the under:
```Token
'i!$!1s%4kzi%q(_^9b$i&!&apwu1!)l#=x0429(6m=7+i(ajtm'
```
It's used to make the password for every account.(Salt)
### 配置Redis
Django默认的settings.py(./src/SQL_memOJi/settings.py)中有下述两行连接Redis的操作，若Redis设置的有密码，请修改相应链接即可。还需要在./src/SQL_memOJi/celery.py文件中修改相应Redis broker地址。
``` bash
broker_url = 'redis://127.0.0.1:6379/0'
result_backend = 'redis://127.0.0.1:6379/1'
```
### Start 启动
``` shell
python3 manage.py makemigrations coding user
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver ip:端口
```
### Create Superuser
``` shell
python3 manage.py createsuperuser
```
### Create A New School
超级用户登录，按照要求新建学校，默认信息即为西北工业大学。
### Create A Teacher
#### 新建用户与新增教师身份
Login the admin page(http://ip:port/admin) with superuser identity.New a school info.
超级用户不能赋予教师和学生身份，因此需要重新在后台注册一个新用户(后台位置：User -> 用户http://yourhost/admin/user/user/add/)，并在后台给该用户新增教师身份(后台位置：User -> 教师)。

#### 设置组权限
超级管理员登录，选择左侧认证和授权->组 栏目增加一个新的用户组，组的名字命名为普通教师(可随意)，并给予如下权限。
- 考试 增删改查(Add Change Delete View)
- 考试作答记录 增删改查(Add Change Delete View)
- 题目作答记录（考试） 增删改查(Add Change Delete View)
- 练习作答记录 增删改查(Add Change Delete View)
- 题目作答记录（练习） 增删改查(Add Change Delete View)
- 试卷 增删改查(Add Change Delete View)
- 题目 增删改查(Add Change Delete View)
- 题库 增删改查(Add Change Delete View)
<!-- - 内容类型 增删改查(Add Change Delete View)
- 会话 增删改查(Add Change Delete View) -->
- 班级 增删改查(Add Change Delete View)
- 学校 查(View)
- 学生 增删改查(Add Change Delete View)
- 用户 增删改查(Add Change Delete View)
PS:实际上不给予组权限和相关用户的权限即可。同时不要给予新建学校等的权限。如果无所谓其实可以全给，后台已经做过限制。并将该权限赋予该名老师，同时给予给老师工作人员状态(Staff权限若在前台网页注册时已经自动赋予)权限。(Staff权限若在前台网页注册时已经自动赋予)
### 新建班级
接下来即可新建一个班级，班级则可以直接通过新注册的教师账号进行创建，需要注意的是，我们需要指定一个**班级识别码**,并将该识别码分发给学生完成身份的注册。
### 新建题库
首先需要新建一个题库，需要注意的是数据库名称和创建SQL的信息，数据库名称是这个题库中题目在哪个数据库内进行SQL操作，创建SQL则是说在这个SQL创建时需要执行什么语句。
### 新建题目
选择题库新建题目即可。
### 新建试卷
通过选择题目并设定分值完成该步骤。**由于Django-admin的限制，请不要在同张试卷中加入重复添加相同题目，会导致程序崩溃！**
### 新建考试/练习
练习和考试的区别：考试只能提交一次，练习可以无限次数的提交。
考试在截止后才能看到参考答案，而练习在提交后即可看到。

### 任务队列
#### 原理
使用Celery完成了两个操作：
- 按需轮流判题
题目按照提交的顺序提交到队列中进行判题。
- 定时阅卷
每隔20秒查阅当前已提交但是没有批改的试卷，并对其进行批改。
#### 配置操作
需要手动打开Celery(首先已经配置好了Redis)
```bash
# 在src目录下执行下述命令 已经启动Django的情况下
# 打卡判题的队列
celery -A SQL_memOJi worker -l info
# 打开定时判卷任务
celery -A SQL_memOJi beat
```
### End
Author:Seddon(Mail:seddon@mail.nwpu.edu.cn)
欢迎各种提问。
