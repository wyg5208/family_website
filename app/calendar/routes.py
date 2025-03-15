from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app import db
from app.calendar import bp
from app.calendar.forms import ScheduleForm
from app.models import Schedule
from datetime import datetime, timedelta

@bp.route('/')
@login_required
def index():
    """显示日历视图"""
    # 获取当前月份的所有日程
    today = datetime.utcnow()
    start_of_month = datetime(today.year, today.month, 1)
    if today.month == 12:
        end_of_month = datetime(today.year + 1, 1, 1) - timedelta(days=1)
    else:
        end_of_month = datetime(today.year, today.month + 1, 1) - timedelta(days=1)
    
    schedules = Schedule.query.filter(
        Schedule.user_id == current_user.id,
        Schedule.start_time >= start_of_month,
        Schedule.start_time <= end_of_month
    ).order_by(Schedule.start_time).all()
    
    return render_template('calendar/index.html', 
                          title='家庭日程',
                          schedules=schedules,
                          today=today,
                          start_of_month=start_of_month,
                          end_of_month=end_of_month,
                          current_year=datetime.now().year)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_schedule():
    """创建新日程"""
    form = ScheduleForm()
    if form.validate_on_submit():
        schedule = Schedule(
            title=form.title.data,
            description=form.description.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            all_day=form.all_day.data,
            reminder=form.reminder.data,
            reminder_time=form.reminder_time.data if form.reminder.data else None,
            user_id=current_user.id
        )
        db.session.add(schedule)
        db.session.commit()
        flash('日程创建成功！')
        return redirect(url_for('calendar.index'))
    return render_template('calendar/create.html', title='添加日程', form=form, current_year=datetime.now().year)

@bp.route('/<int:schedule_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_schedule(schedule_id):
    """编辑日程"""
    schedule = Schedule.query.get_or_404(schedule_id)
    if schedule.user_id != current_user.id:
        abort(403)
    
    form = ScheduleForm()
    if form.validate_on_submit():
        schedule.title = form.title.data
        schedule.description = form.description.data
        schedule.start_time = form.start_time.data
        schedule.end_time = form.end_time.data
        schedule.all_day = form.all_day.data
        schedule.reminder = form.reminder.data
        schedule.reminder_time = form.reminder_time.data if form.reminder.data else None
        
        db.session.commit()
        flash('日程更新成功！')
        return redirect(url_for('calendar.index'))
    elif request.method == 'GET':
        form.title.data = schedule.title
        form.description.data = schedule.description
        form.start_time.data = schedule.start_time
        form.end_time.data = schedule.end_time
        form.all_day.data = schedule.all_day
        form.reminder.data = schedule.reminder
        form.reminder_time.data = schedule.reminder_time
    
    return render_template('calendar/edit.html', title='编辑日程', form=form, schedule=schedule, current_year=datetime.now().year)

@bp.route('/<int:schedule_id>/delete')
@login_required
def delete_schedule(schedule_id):
    """删除日程"""
    schedule = Schedule.query.get_or_404(schedule_id)
    if schedule.user_id != current_user.id:
        abort(403)
    
    db.session.delete(schedule)
    db.session.commit()
    flash('日程已删除')
    return redirect(url_for('calendar.index'))

@bp.route('/upcoming')
@login_required
def upcoming():
    """显示即将到来的日程"""
    today = datetime.utcnow()
    next_week = today + timedelta(days=7)
    
    upcoming_schedules = Schedule.query.filter(
        Schedule.user_id == current_user.id,
        Schedule.start_time >= today,
        Schedule.start_time <= next_week
    ).order_by(Schedule.start_time).all()
    
    return render_template('calendar/upcoming.html', 
                          title='即将到来的日程',
                          schedules=upcoming_schedules,
                          current_year=datetime.now().year)
