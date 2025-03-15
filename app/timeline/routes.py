import os
from flask import render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.timeline import bp
from app.timeline.forms import EventForm
from app.models import Event
import uuid
from datetime import datetime

def save_image(file):
    if file and file.filename:
        filename = secure_filename(file.filename)
        # 使用UUID生成唯一文件名
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return unique_filename
    return None

@bp.route('/')
def index():
    """显示时间轴"""
    events = Event.query.order_by(Event.date.desc()).all()
    # 按年份分组事件
    events_by_year = {}
    for event in events:
        year = event.date.year
        if year not in events_by_year:
            events_by_year[year] = []
        events_by_year[year].append(event)
    
    # 按年份降序排序
    sorted_years = sorted(events_by_year.keys(), reverse=True)
    
    return render_template('timeline/index.html', 
                          title='家庭大事记',
                          events_by_year=events_by_year,
                          sorted_years=sorted_years,
                          current_year=datetime.now().year)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    """创建新事件"""
    form = EventForm()
    if form.validate_on_submit():
        image_filename = save_image(form.image.data) if form.image.data else None
        
        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            image=image_filename,
            user_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash('事件创建成功！')
        return redirect(url_for('timeline.index'))
    return render_template('timeline/create.html', title='添加事件', form=form, current_year=datetime.now().year)

@bp.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    """编辑事件"""
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)
    
    form = EventForm()
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.date = form.date.data
        
        if form.image.data:
            # 删除旧图片
            if event.image:
                try:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], event.image))
                except:
                    pass
            # 保存新图片
            event.image = save_image(form.image.data)
        
        db.session.commit()
        flash('事件更新成功！')
        return redirect(url_for('timeline.index'))
    elif request.method == 'GET':
        form.title.data = event.title
        form.description.data = event.description
        form.date.data = event.date
    
    return render_template('timeline/edit.html', title='编辑事件', form=form, event=event, current_year=datetime.now().year)

@bp.route('/<int:event_id>/delete')
@login_required
def delete_event(event_id):
    """删除事件"""
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)
    
    # 删除事件图片
    if event.image:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], event.image))
        except:
            pass
    
    db.session.delete(event)
    db.session.commit()
    flash('事件已删除')
    return redirect(url_for('timeline.index')) 