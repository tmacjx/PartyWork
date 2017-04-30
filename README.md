# PartyWork
基于web的计算机学院党务工作管理系统
Flask Bootstrap
Flask-admin

版本
Python3.5
Flask


virtualenv虚拟环境安装
参考: http://www.nowamagic.net/academy/detail/1330228

启动虚拟环境 source 虚拟环境目录/bin/activate

安装依赖
pip -r requirements.txt


初始化数据库
python manage.py init
python manage.py migrate
python manage.py upgrade


初始化角色类型:  普通用户 管理员
并新建一个管理员用户
python manage.py shell

>> Role.insert_role()

>> admin = Role.query.get(name='Administrator')

>> user = User(username='root', email='root@qq.com', password='123456', role=admin)

>> db.session.add(user)

>> db.session.commit()

后台管理路径
/admin