先运行app.py文件作为后端 python app.py
再启动Django python manage.py runserver
报错可能：
1.需要配置个人的mysql数据库并在settings中修改对应设置
2.更新model模型后需要进行迁移至数据库
3.端口占用