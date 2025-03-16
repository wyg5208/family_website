# 家庭网站

这是一个基于Flask的家庭网站，用于管理家庭相册、大事记和日程安排。

## 功能特点

1. **用户管理**：注册、登录和个人资料管理
2. **相册管理**：创建相册、上传照片、查看照片
3. **家庭大事记**：以时间轴方式记录和展示家庭重要事件
4. **日程管理**：创建、编辑和删除家庭日程，支持日程提醒功能
5. **主题切换**：支持明亮模式和深色模式，默认为深色模式
6. **色彩配置**：支持蓝色系、紫色系、灰色系和绿色系四种色彩主题
7. **响应式设计**：适配各种设备屏幕大小

   
首页截图

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b946c44b302b41d38cd840410527ff24.png#pic_center)

## 技术栈

- **后端**：Flask、SQLAlchemy、Flask-Login
- **前端**：HTML、CSS、JavaScript、Bootstrap 5
- **数据库**：SQLite（可扩展至MySQL或PostgreSQL）
- **主题管理**：使用Bootstrap 5的主题系统和localStorage实现主题持久化
- **色彩配置**：使用CSS变量和自定义属性实现多色彩主题

## 详细安装与部署指南

### 系统要求

- Python 3.8+
- pip 包管理器
- Git（可选，用于克隆项目）
- 足够的磁盘空间用于存储照片和其他媒体文件

### 开发环境部署

1. **克隆或下载项目**

   ```bash
   git clone https://github.com/yourusername/family_website.git
   cd family_website
   ```

   或者下载ZIP文件并解压。

2. **创建并激活虚拟环境**

   在Windows上:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   在macOS/Linux上:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**

   创建`.env`文件在项目根目录，添加以下内容：

   ```
   FLASK_APP=family_website.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///app.db
   MAIL_SERVER=smtp.example.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@example.com
   MAIL_PASSWORD=your-email-password
   ```

   请替换为您自己的值，特别是`SECRET_KEY`、邮件服务器和凭据。

5. **初始化数据库**

   ```bash
   flask db init
   flask db migrate -m "initial migration"
   flask db upgrade
   ```

6. **创建上传目录**

   确保上传目录存在并具有正确的权限：

   ```bash
   mkdir -p app/static/uploads/photos
   mkdir -p app/static/uploads/carousel
   mkdir -p app/static/uploads/timeline
   ```

7. **运行开发服务器**

   ```bash
   flask run
   ```

   现在您可以在浏览器中访问 http://127.0.0.1:5000/ 查看网站。

### 生产环境部署

#### 使用Gunicorn和Nginx（Linux服务器）

1. **安装Gunicorn**

   ```bash
   pip install gunicorn
   ```

2. **创建Gunicorn服务文件**

   创建文件 `/etc/systemd/system/family_website.service`：

   ```ini
   [Unit]
   Description=Gunicorn instance to serve family website
   After=network.target

   [Service]
   User=your_username
   Group=www-data
   WorkingDirectory=/path/to/family_website
   Environment="PATH=/path/to/family_website/venv/bin"
   ExecStart=/path/to/family_website/venv/bin/gunicorn --workers 3 --bind unix:family_website.sock -m 007 wsgi:app

   [Install]
   WantedBy=multi-user.target
   ```

   替换 `your_username` 和路径为您的实际值。

3. **创建wsgi.py文件**

   在项目根目录创建 `wsgi.py`：

   ```python
   from family_website import app

   if __name__ == "__main__":
       app.run()
   ```

4. **配置Nginx**

   创建文件 `/etc/nginx/sites-available/family_website`：

   ```nginx
   server {
       listen 80;
       server_name your_domain.com www.your_domain.com;

       location / {
           include proxy_params;
           proxy_pass http://unix:/path/to/family_website/family_website.sock;
       }

       location /static {
           alias /path/to/family_website/app/static;
       }
   }
   ```

   启用站点并重启Nginx：

   ```bash
   sudo ln -s /etc/nginx/sites-available/family_website /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

5. **启动服务**

   ```bash
   sudo systemctl start family_website
   sudo systemctl enable family_website
   ```

#### 使用Docker部署

1. **创建Dockerfile**

   在项目根目录创建 `Dockerfile`：

   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   RUN pip install gunicorn

   COPY . .

   RUN mkdir -p app/static/uploads/photos
   RUN mkdir -p app/static/uploads/carousel
   RUN mkdir -p app/static/uploads/timeline

   ENV FLASK_APP=family_website.py
   ENV FLASK_ENV=production

   EXPOSE 5000

   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
   ```

2. **创建docker-compose.yml**

   ```yaml
   version: '3'
   services:
     web:
       build: .
       ports:
         - "5000:5000"
       volumes:
         - ./app/static/uploads:/app/app/static/uploads
       environment:
         - SECRET_KEY=your-secret-key
         - DATABASE_URL=sqlite:///app.db
         - MAIL_SERVER=smtp.example.com
         - MAIL_PORT=587
         - MAIL_USE_TLS=True
         - MAIL_USERNAME=your-email@example.com
         - MAIL_PASSWORD=your-email-password
       restart: always
   ```

3. **构建和运行容器**

   ```bash
   docker-compose up -d
   ```

## 初始配置

成功部署网站后，需要进行以下初始配置：

1. **创建管理员账户**

   访问网站注册页面，创建第一个用户账户。然后通过数据库将该用户设置为管理员：

   ```bash
   flask shell
   ```

   在shell中执行：

   ```python
   from app import db
   from app.models import User
   user = User.query.filter_by(username='your_username').first()
   user.is_admin = True
   db.session.commit()
   exit()
   ```

2. **配置轮播图**

   登录管理员账户后，访问轮播图管理页面，添加首页轮播图。

3. **配置邮件通知**

   确保在`.env`文件中正确配置了邮件服务器信息，以启用邮件通知功能。

4. **设置备份策略**

   建议定期备份数据库和上传的文件：

   ```bash
   # 备份数据库
   cp app/app.db backups/app_$(date +%Y%m%d).db

   # 备份上传的文件
   tar -czf backups/uploads_$(date +%Y%m%d).tar.gz app/static/uploads/
   ```

   可以将此命令添加到crontab中实现自动备份。

## 使用说明

1. **注册和登录**
   - 访问网站首页，点击"注册"按钮
   - 填写用户名、电子邮件和密码
   - 注册成功后，使用凭据登录

2. **相册管理**
   - 点击导航栏中的"相册"
   - 创建新相册：点击"创建相册"按钮，填写标题和描述
   - 上传照片：在相册页面点击"上传照片"，选择文件并添加描述
   - 管理照片：可以编辑、删除照片，或设置为相册封面

3. **时间线管理**
   - 点击导航栏中的"时间线"
   - 添加事件：点击"添加事件"按钮，填写事件详情和日期
   - 可以按时间顺序查看所有家庭重要事件

4. **日历管理**
   - 点击导航栏中的"日历"
   - 添加日程：点击日期或"添加日程"按钮，填写日程详情
   - 查看日程：可以按月、周、日查看日程安排

5. **主题切换**
   - 点击导航栏右上角的主题切换按钮
   - 在深色模式和明亮模式之间切换
   - 设置会自动保存，下次访问时应用

6. **色彩配置**
   - 点击导航栏右上角的色彩配置下拉菜单
   - 选择喜欢的色彩主题：蓝色系、紫色系、灰色系或绿色系
   - 设置会自动保存，下次访问时应用

## 主题与色彩功能

网站支持两种主题模式和四种色彩配置：

### 主题模式
- **深色模式（默认）**：适合夜间浏览，减轻眼睛疲劳
- **明亮模式**：适合日间浏览，提供传统的浏览体验

### 色彩主题
- **蓝色系（默认）**：经典的蓝色调，给人稳重、专业的感觉
- **紫色系**：优雅的紫色调，给人创意、神秘的感觉
- **灰色系**：简约的灰色调，给人沉稳、商务的感觉
- **绿色系**：清新的绿色调，给人自然、和谐的感觉

色彩主题会全面应用于整个网站的各个元素，包括：
- 导航栏背景和文字
- 按钮和链接
- 卡片标题和边框
- 图标和强调元素
- 时间线的线条和日期标签
- 日历的事件和当天高亮
- 表单元素和交互组件

主题和色彩设置会保存在浏览器的localStorage中，下次访问时会自动应用上次选择的设置。

## 故障排除

1. **数据库迁移问题**
   
   如果遇到数据库迁移错误，尝试：
   ```bash
   flask db stamp head
   flask db migrate
   flask db upgrade
   ```

2. **上传文件权限问题**
   
   确保上传目录具有正确的权限：
   ```bash
   chmod -R 755 app/static/uploads
   ```

3. **邮件发送失败**
   
   检查邮件服务器配置，确保没有被防火墙阻止。

4. **网站加载缓慢**
   
   - 优化上传的图片大小
   - 考虑使用CDN服务
   - 检查数据库索引

## 项目结构

```
family_website/
├── app/                    # 应用主目录
│   ├── static/             # 静态文件
│   │   ├── css/            # CSS样式文件
│   │   ├── js/             # JavaScript文件
│   │   │   ├── theme.js    # 主题切换功能
│   │   │   └── color-theme.js # 色彩主题切换功能
│   │   └── uploads/        # 上传的文件
│   ├── templates/          # HTML模板
│   ├── main/               # 主页蓝图
│   ├── auth/               # 认证蓝图
│   ├── album/              # 相册蓝图
│   ├── timeline/           # 时间轴蓝图
│   ├── calendar/           # 日程蓝图
│   ├── models.py           # 数据库模型
│   └── __init__.py         # 应用初始化
├── migrations/             # 数据库迁移文件
├── config.py               # 配置文件
├── family_website.py       # 应用入口
├── wsgi.py                 # WSGI入口点（用于生产部署）
├── Dockerfile              # Docker配置文件
├── docker-compose.yml      # Docker Compose配置
├── requirements.txt        # 依赖包列表
└── .env                    # 环境变量配置（不应提交到版本控制）
```

## 性能优化建议

1. **图片优化**
   - 在上传前压缩图片
   - 生成并使用缩略图进行预览
   - 考虑使用延迟加载技术

2. **数据库优化**
   - 为常用查询添加索引
   - 定期清理不需要的数据
   - 考虑使用更强大的数据库（如PostgreSQL）

3. **缓存策略**
   - 使用Redis缓存频繁访问的数据
   - 启用静态文件缓存

## 安全建议

1. **定期更新依赖**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **启用HTTPS**
   - 使用Let's Encrypt获取免费SSL证书
   - 配置Nginx强制使用HTTPS

3. **定期备份**
   - 数据库备份
   - 上传文件备份

4. **限制上传文件类型和大小**
   - 已在应用中实现，但可根据需要调整

## 未来计划

- 添加家庭成员管理功能
- 集成家庭财务管理
- 添加家庭聊天功能
- 支持多语言
- 增加更多主题选项和色彩配置
- 添加API接口，支持移动应用
- 集成家庭智能设备控制

## 贡献指南

欢迎贡献代码或提出建议！请遵循以下步骤：

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证 - 详情请参阅LICENSE文件。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 电子邮件：your.email@example.com
- GitHub Issues：[提交问题](https://github.com/yourusername/family_website/issues)
