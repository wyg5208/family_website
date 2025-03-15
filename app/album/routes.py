import os
from flask import render_template, redirect, url_for, flash, request, current_app, abort, jsonify
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.album import bp
from app.album.forms import AlbumForm, PhotoForm
from app.models import Album, Photo
import uuid
from datetime import datetime

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_photo(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 使用UUID生成唯一文件名
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        # 确保photos子文件夹存在
        photos_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos')
        if not os.path.exists(photos_folder):
            os.makedirs(photos_folder)
        # 保存到photos子文件夹
        file_path = os.path.join(photos_folder, unique_filename)
        file.save(file_path)
        return 'photos/' + unique_filename
    return None

@bp.route('/')
def index():
    """显示所有相册"""
    albums = Album.query.order_by(Album.created_at.desc()).all()
    return render_template('album/index.html', title='相册', albums=albums, current_year=datetime.now().year)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_album():
    """创建新相册"""
    form = AlbumForm()
    if form.validate_on_submit():
        album = Album(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(album)
        db.session.commit()
        flash('相册创建成功！', 'success')
        return redirect(url_for('album.view_album', album_id=album.id))
    return render_template('album/create.html', title='创建相册', form=form, current_year=datetime.now().year)

@bp.route('/<int:album_id>')
def view_album(album_id):
    """查看单个相册"""
    album = Album.query.get_or_404(album_id)
    
    # 如果用户未登录或不是相册所有者，只显示非私密照片
    if not current_user.is_authenticated or current_user.id != album.user_id:
        photos = album.photos.filter_by(is_private=False).order_by(Photo.uploaded_at.desc()).all()
    else:
        photos = album.photos.order_by(Photo.uploaded_at.desc()).all()
        
    return render_template('album/view.html', title=album.title, album=album, photos=photos, current_year=datetime.now().year)

@bp.route('/<int:album_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_album(album_id):
    """编辑相册"""
    album = Album.query.get_or_404(album_id)
    if album.user_id != current_user.id:
        abort(403)
    
    form = AlbumForm()
    if form.validate_on_submit():
        album.title = form.title.data
        album.description = form.description.data
        
        # 处理封面照片
        cover_photo_id = request.form.get('cover_photo')
        if cover_photo_id:
            album.cover_photo_id = int(cover_photo_id)
        else:
            album.cover_photo_id = None
            
        db.session.commit()
        flash('相册更新成功！', 'success')
        return redirect(url_for('album.view_album', album_id=album.id))
    
    # 填充表单
    form.title.data = album.title
    form.description.data = album.description
    
    return render_template('album/edit.html', title='编辑相册', form=form, album=album, current_year=datetime.now().year)

@bp.route('/<int:album_id>/upload', methods=['GET', 'POST'])
@login_required
def upload_photo(album_id):
    """上传照片到相册"""
    album = Album.query.get_or_404(album_id)
    if album.user_id != current_user.id:
        abort(403)
    
    form = PhotoForm()
    if form.validate_on_submit():
        uploaded_files = request.files.getlist('photos')
        if uploaded_files:
            success_count = 0
            for file in uploaded_files:
                filename = save_photo(file)
                if filename:
                    photo = Photo(
                        filename=filename,
                        title=form.title.data if hasattr(form, 'title') else None,
                        description=form.description.data,
                        album_id=album.id,
                        is_private=form.is_private.data
                    )
                    db.session.add(photo)
                    success_count += 1
            
            if success_count > 0:
                db.session.commit()
                if success_count == 1:
                    flash('1张照片上传成功！', 'success')
                else:
                    flash(f'{success_count}张照片上传成功！', 'success')
                return redirect(url_for('album.view_album', album_id=album.id))
            else:
                flash('上传失败，请确保文件格式正确', 'danger')
        else:
            flash('请选择至少一张照片', 'warning')
    
    return render_template('album/upload.html', title='上传照片', form=form, album=album, current_year=datetime.now().year)

@bp.route('/<int:album_id>/delete')
@login_required
def delete_album(album_id):
    """删除相册"""
    album = Album.query.get_or_404(album_id)
    if album.user_id != current_user.id:
        abort(403)
    
    # 删除相册中的所有照片文件
    for photo in album.photos:
        try:
            photos_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos')
            # 获取文件名（不包含路径）
            filename = photo.filename.split('/')[-1] if '/' in photo.filename else photo.filename
            os.remove(os.path.join(photos_folder, filename))
        except Exception as e:
            current_app.logger.error(f"删除照片文件失败: {str(e)}")
    
    db.session.delete(album)
    db.session.commit()
    flash('相册已删除', 'success')
    return redirect(url_for('album.index'))

@bp.route('/photo/<int:photo_id>/delete')
@login_required
def delete_photo(photo_id):
    """删除照片"""
    photo = Photo.query.get_or_404(photo_id)
    if photo.album.user_id != current_user.id:
        abort(403)
    
    album_id = photo.album_id
    
    # 删除照片文件
    try:
        photos_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos')
        # 获取文件名（不包含路径）
        filename = photo.filename.split('/')[-1] if '/' in photo.filename else photo.filename
        os.remove(os.path.join(photos_folder, filename))
    except Exception as e:
        current_app.logger.error(f"删除照片文件失败: {str(e)}")
    
    db.session.delete(photo)
    db.session.commit()
    flash('照片已删除', 'success')
    return redirect(url_for('album.view_album', album_id=album_id))

@bp.route('/api/photos/<int:album_id>')
def api_album_photos(album_id):
    """API端点：获取相册中的照片，用于幻灯片功能"""
    album = Album.query.get_or_404(album_id)
    
    # 如果用户未登录或不是相册所有者，只返回非私密照片
    if not current_user.is_authenticated or current_user.id != album.user_id:
        photos = album.photos.filter_by(is_private=False).order_by(Photo.uploaded_at.desc()).all()
    else:
        photos = album.photos.order_by(Photo.uploaded_at.desc()).all()
    
    # 将照片数据转换为JSON格式
    photos_data = []
    for photo in photos:
        photos_data.append({
            'id': photo.id,
            'filename': photo.filename,
            'title': photo.title,
            'description': photo.description
        })
    
    return jsonify({'photos': photos_data}) 