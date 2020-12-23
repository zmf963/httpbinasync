# 开发杂记

## httpbin简单分析

代码量：

```bash
root@node:/opt/httpbinasync/tmp/httpbin# cloc .
      36 text files.
      35 unique files.                              
      14 files ignored.

github.com/AlDanial/cloc v 1.74  T=0.13 s (179.0 files/s, 32138.8 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                           8            518           1012           1762
HTML                             7            107              2            592
YAML                             2              3              0             23
JSON                             2              0              0             19
Markdown                         1             12              0             19
XML                              1              5              3             16
Dockerfile                       1              7              0             15
INI                              1              2              0             13
-------------------------------------------------------------------------------
SUM:                            23            654           1017           2459
-------------------------------------------------------------------------------
```

不太多的样子,准备看一下然后用sanic重写一遍，熟悉下sanic又是一年多没怎么写过了


项目依赖:

pipenv gunicorn flask gevent
```bash
gunicorn = "*"  WSGI HTTP服务器
decorator = "*" 方便使用装饰器
brotlipy = "*" Brotli压缩算法
gevent = "*" 基于协程的并发库
Flask = "*"  web框架
meinheld = "*"  异步 WSGI Web 服务器
werkzeug = ">=0.14.1" wsgi工具包，flask依赖
six = "*"  py2、3兼容的模块
flasgger = "*"   生成api文档
pyyaml = {git = "https://github.com/yaml/pyyaml.git"}
```

目录结构：

```bash
root@node:/opt/httpbinasync/tmp/httpbin# tree
.
├── app.json
├── AUTHORS
├── docker-compose.yml
├── Dockerfile
├── httpbin  # 主要代码目录
│   ├── core.py # 代码入口
│   ├── filters.py
│   ├── helpers.py
│   ├── __init__.py
│   ├── static
│   │   └── favicon.ico
│   ├── structures.py
│   ├── templates  # jinja2模板文件
│   │   ├── flasgger
│   │   │   └── index.html
│   │   ├── footer.html
│   │   ├── forms-post.html
│   │   ├── httpbin.1.html
│   │   ├── images
│   │   │   ├── jackal.jpg
│   │   │   ├── pig_icon.png
│   │   │   ├── svg_logo.svg
│   │   │   └── wolf_1.webp
│   │   ├── index.html
│   │   ├── moby.html
│   │   ├── sample.xml
│   │   ├── trackingscripts.html
│   │   └── UTF-8-demo.txt
│   ├── utils.py
│   └── VERSION
├── LICENSE
├── MANIFEST.in
├── now.json
├── Pipfile
├── Pipfile.lock
├── Procfile
├── README.md
├── runtime.txt
├── setup.cfg
├── setup.py
├── test_httpbin.py  项目的单元测试文件 使用unittest
└── tox.ini
```