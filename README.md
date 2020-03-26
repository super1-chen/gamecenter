# gamecenter-api

游戏平台api的代码，本项目使用python2.7.16开发，其它版本的python没有经过测试，请小心使用, 服务器为centos 6.9

## app说明

项目采用python2.7进行开发，使用到数据库为

1. mysql 使用sqlalchmey连接数据库
2. mongodb 使用mongoengine 连接项目
3. 数据库连接全部采用url方式配置，数据库需要单独配置

使用到的依赖查询

## 安装部署

### 安装gcc

```shell
$ yum install gcc openssl-devel bzip2-devel
```

### 安装python2.7.16

下载python

参考文档[How to Install Python 2.7.16 on CentOS/RHEL 7/6 and Fedora 30-25](https://tecadmin.net/install-python-2-7-on-centos-rhel/)

```shell
$ cd /usr/src
$ wget https://www.python.org/ftp/python/2.7.16/Python-2.7.16.tgz
$ tar xzf Python-2.7.16.tgz
```

安装python

```shell
$ cd Python-2.7.16
$ ./configure --enable-optimizations
$ make altinstall
```

安装pip

```shell
$ curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
$ python2.7 get-pip.py
```

### 安装supervisord


```shell
$ cd /etc/yum.repos.d/
$ vim fxdata.repo
```

把下面的内容贴上去

```shell
[fxdata]
name=fxdata repo
baseurl=https://fxdata-yum.oss-cn-shanghai.aliyuncs.com/
gpgcheck=0
enabled=1
```

保存退出

```shell
$ yum --enablerepo=fxdata install supervisor
```

### 安装项目

下载代码

项目托管在github上面，直接拉去代码到服务器的`/home` 下面

#### 创建虚拟环境和安装的

```shell
$ pip install virtualenv
$ virtualenv game_venv -p /usr/local/bin/python2.7
$ source game_venv/bin/activate
```

安装依赖项目依赖

```shell
cd /home/game_center && pip install -e .
```

修改config

在/home/gamecenter/etc 目录中有三个文件

```shell
gamecenter_api.ini
gamecenter.conf.sample
nginx_gamecenter.conf
```

1. gamecenter_api.ini supervisor 进程管理控制文件
2. gamecenter.conf.sample app 配置文件样本
3. nginx_gamecenter.conf nginx config的文件的

### 修改app的配置文

```shell
$ mv gamecenter.conf.sample gamecenter.conf
```

修改下面的内容
```
[DEFAULT]
# whether enable debug logging
debug = false

[DB]
# datebase url that xedge itself maintained
sql_connection = mysql://root@localhost/gamecenter

[MONGODB]
# mongo address url
mongo_connection = mongodb://username:password@localhost:27017?authSource=admin

[SDK]
# sdk keys
cp_game_key = abcdsaer12
# # skd host
host = http://fw.dewaeaf2.com
```
修改对应的配置的保存退出

### 安装数据库和升级数据库

mysql中需要创建一个名字为`gamecenter` 的数据库

```mysql
CREATE DATABASE IF NOT EXISTS `gamecenter` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
```

数据库采用sqlalcehmy模型和alembic文件托管，alembic文件模型和项目一起打包在代码中，

完成项目安装之后

```shell
$ source /home/game_venv/bin/activate
$ (game_venv) $ game-manage upgrade head
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
```

关于`game-manage` 项目命令行工具下面会详细说明

### 修改supervisor.conf

#### 生成默认配置项目

```shell
$ echo_supervisord_conf > /etc/supervisord.conf
```
创建文夹

```shell
$ mkdir /etc/supervisord.d
```
移动文件/home/gamecenter/etc/\*.ini 这些文件到上面创建的文件夹中

修改`/etc/supervisord.conf` 最下面的内容

```
[include]
files = supervisord.d/*.ini
```
完成上述配置，执行

```shell
$ supervisorctl upgdate
```

检查进程是否起来

```$
$ ps -ef | grep game-api
root     13998  9590  0 Mar25 ?        00:05:16 /home/game_venv/bin/python /home/game_venv/bin/game-api --port=8005
root     13999  9590  0 Mar25 ?        00:05:33 /home/game_venv/bin/python /home/game_venv/bin/game-api --port=8004
root     14012  9590  0 Mar25 ?        00:04:48 /home/game_venv/bin/python /home/game_venv/bin/game-api --port=8007
root     14019  9590  0 Mar25 ?        00:04:50 /home/game_venv/bin/python /home/game_venv/bin/game-api --port=8006
```
出现上面的结果表示已经起来了

### nginx 配置

app默认开放本地端口8004-8007四个端口，需要使用nginx做内部负载均衡，具体参考`/etc/nginx_gamecenter.conf`

### 配置app的nginx.conf


```mv
$ cd /home/nginx/conf.d && mv default.conf default.conf.bak
```
将app中nginx配置文件移动到的 `/home/nginx/conf.d`

执行命令

```
$ service nginx reload
Reloading nginx:                                           [  OK  ]
```

按照上面的配置完成可以使用服务器的80端口访问app

```
curl localhost/v1
{"status": "success"}
```

## 项目cmd 入口

该项目一共有三个入口

1. game-api app api的主要入口
2. game-manage 用来做一些命令行工具的操作
3. game-worker 定时任务的入口（还在开发）

### game-api

```shell
$ game-api --help
usage: game-api [-h] [-p PORT] [-a ADDRESS] [-c CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  run on the give port
  -a ADDRESS, --address ADDRESS
                        run on the give address
  -c CONFIG, --config CONFIG
                        use specific config file

```

|参数|说明|
|----|----|
|`-p`|  port端口 默认 8000|
|`-a`| host address 默认 127.0.0.1|
|`-c`| config 文件的地址 默认app 根目录下的 etc中的gamecenter.conf|





## 参考文档

1. [How to Install Python 2.7.16 on CentOS/RHEL 7/6 and Fedora 30-25](https://tecadmin.net/install-python-2-7-on-centos-rhel/)
