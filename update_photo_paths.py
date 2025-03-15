from app import create_app, db
from app.models import Photo

app = create_app()
with app.app_context():
    photos = Photo.query.all()
    print(f"总共有 {len(photos)} 张照片")
    
    for photo in photos:
        # 如果照片路径不包含'photos/'前缀，则添加
        if not photo.filename.startswith('photos/'):
            # 保存原始文件名
            original_filename = photo.filename
            # 更新为新格式
            photo.filename = f"photos/{original_filename}"
            print(f"更新照片 ID: {photo.id}, 从 {original_filename} 到 {photo.filename}")
    
    # 提交更改
    db.session.commit()
    print("照片路径更新完成") 