from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # 获取用户名为 'admin' 的用户，如果不存在则创建
    user = User.query.filter_by(username='admin').first()
    
    if not user:
        # 创建管理员用户
        user = User(username='admin', email='admin@example.com', is_admin=True)
        user.set_password('admin123')
        db.session.add(user)
        print("创建管理员用户: admin (密码: admin123)")
    else:
        # 将现有用户设置为管理员
        user.is_admin = True
        print(f"将用户 {user.username} 设置为管理员")
    
    db.session.commit()
    print("操作完成！") 