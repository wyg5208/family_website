import os
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.main import bp
from app.main.forms import CarouselForm, CarouselEditForm
from app.models import Photo, Event, TimelineEvent, Carousel, CalendarEvent
import uuid
from datetime import datetime, timedelta

def save_image(file):
    if file and file.filename:
        filename = secure_filename(file.filename)
        # 使用UUID生成唯一文件名
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # 确保目录存在
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'carousel')
        os.makedirs(upload_path, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(upload_path, unique_filename)
        file.save(file_path)
        
        # 返回相对于static/uploads的路径，使用正斜杠
        return 'carousel/' + unique_filename
    return None

@bp.route('/')
def index():
    # 获取最新照片
    recent_photos = Photo.query.order_by(Photo.uploaded_at.desc()).limit(4).all()
    
    # 获取即将到来的事件
    upcoming_events = CalendarEvent.query.filter(CalendarEvent.start_time >= datetime.now()).order_by(CalendarEvent.start_time).limit(3).all()
    
    # 获取最近的时间线事件
    recent_timeline_events = TimelineEvent.query.order_by(TimelineEvent.created_at.desc()).limit(3).all()
    
    # 获取轮播图
    carousels = Carousel.query.filter_by(active=True).order_by(Carousel.order).all()
    
    return render_template('main/index.html', 
                          recent_photos=recent_photos,
                          upcoming_events=upcoming_events,
                          recent_timeline_events=recent_timeline_events,
                          carousels=carousels)

@bp.route('/carousel')
@login_required
def carousel_list():
    if not current_user.is_admin:
        flash('只有管理员可以管理轮播图', 'danger')
        return redirect(url_for('main.index'))
    
    carousels = Carousel.query.order_by(Carousel.order).all()
    return render_template('main/carousel_list.html', carousels=carousels)

@bp.route('/carousel/create', methods=['GET', 'POST'])
@login_required
def carousel_create():
    if not current_user.is_admin:
        flash('只有管理员可以管理轮播图', 'danger')
        return redirect(url_for('main.index'))
    
    form = CarouselForm()
    if form.validate_on_submit():
        image_filename = save_image(form.image.data)
        
        carousel = Carousel(
            title=form.title.data,
            description=form.description.data,
            image=image_filename,
            order=form.order.data,
            active=form.active.data,
            user_id=current_user.id
        )
        
        db.session.add(carousel)
        db.session.commit()
        
        flash('轮播图创建成功！', 'success')
        return redirect(url_for('main.carousel_list'))
    
    return render_template('main/carousel_create.html', form=form)

@bp.route('/carousel/<int:carousel_id>/edit', methods=['GET', 'POST'])
@login_required
def carousel_edit(carousel_id):
    if not current_user.is_admin:
        flash('只有管理员可以管理轮播图', 'danger')
        return redirect(url_for('main.index'))
    
    carousel = Carousel.query.get_or_404(carousel_id)
    form = CarouselEditForm()
    
    if form.validate_on_submit():
        carousel.title = form.title.data
        carousel.description = form.description.data
        carousel.order = form.order.data
        carousel.active = form.active.data
        
        if form.image.data:
            # 删除旧图片
            if carousel.image:
                try:
                    old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], carousel.image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                except Exception as e:
                    current_app.logger.error(f"删除旧图片失败: {str(e)}")
            
            # 保存新图片
            carousel.image = save_image(form.image.data)
        
        db.session.commit()
        flash('轮播图更新成功！', 'success')
        return redirect(url_for('main.carousel_list'))
    
    elif request.method == 'GET':
        form.title.data = carousel.title
        form.description.data = carousel.description
        form.order.data = carousel.order
        form.active.data = carousel.active
    
    return render_template('main/carousel_edit.html', form=form, carousel=carousel)

@bp.route('/carousel/<int:carousel_id>/delete')
@login_required
def carousel_delete(carousel_id):
    if not current_user.is_admin:
        flash('只有管理员可以管理轮播图', 'danger')
        return redirect(url_for('main.index'))
    
    carousel = Carousel.query.get_or_404(carousel_id)
    
    # 删除图片文件
    if carousel.image:
        try:
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], carousel.image)
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            current_app.logger.error(f"删除图片失败: {str(e)}")
    
    db.session.delete(carousel)
    db.session.commit()
    
    flash('轮播图已删除！', 'success')
    return redirect(url_for('main.carousel_list'))