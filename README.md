使用方法

填写必要设置：填写setting.py中的数据库设置、新建.env填入大模型api

运行app.py `python app.py`

运行manage.py `python manage.py runserver`

报错可能：

1. Django数据库模型更改后需要进行迁移（请搜索如何操作）
2. 端口占用，会使用到mysql 3306端口、Django 8000端口、grodio 7860端口
