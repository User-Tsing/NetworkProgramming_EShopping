Directed by STAssn          
网络程序设计：电商平台的设计：DJANGO+JS+HTML+CSS      
实现功能：
实现用户注册、登录、登出功能。     
实现商品信息的展示（列表页、详情页）。     
实现商品搜索功能。     
实现购物车功能（添加商品、查看购物车、从购物车中选择商品进行结算）。     
实现订单生成与支付确认流程（模拟支付，主要关注订单状态流转和库存更新）。      
实现用户个人中心，包括查看/修改个人（基础）信息、管理已发布的商品、查看购买历史。     
实现用户发布商品功能。     
实现用户之间的即时通讯。     
实现购买商品后的评价系统。     

支持移动端访问。       

未实现功能：没有原始商品数据，有需要的可以去网络上挖取相关数据。（为保护个人信息等settings.py、db.sqlite3均未上传，请自行配置）    

配置方式：确认环境配置正常，主要适配django。以下命令均在PyCharm Community（或PyCharm Professional）终端运行      
创建django项目：django-admin startproject  (若为PyCharm Professional在创建项目时选Django)       
配置APP：python manage.py startapp APP_NAME      
配置迁移数据库：python manage.py makemigrations,  python manage.py migrate      
创建超级用户：python manage.py createsuperuser       
运行方式：打开pycharm，进入终端，查看地址确认与manage.py在同一目录，输入： python manage.py runserver，并运行然后进入浏览器运行127.0.0.1:8000          

联机部署：      
settings.py关闭DEBUG，使用ALLOWED_HOSTS = ['*']，终端使用python manage.py runserver 0.0.0.0:8000，在同一局域网内通过服务器机的IP地址访问网站，对服务器机配置有要求。      
使用云端托管网站如PythonAnywhere等，利用账号网页访问网站，但有一定限制。       

自定义配置：     
后端：models.py中设定模型（每次修改须重新迁移数据库），views.py中设定后端交互效果，urls.py中配置路由并绑定views.py中的效果，      
前端：.html文件设定界面模块，.js文件设定界面交互效果，.css文件设定界面版式，其中.html是主要部分，其中有调用对应的.js和.css             

上传是为了纪念做过的课程项目。     
Directed by STAssn     
Participants: Y Yang, H Mao    
