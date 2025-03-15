from flask import Blueprint, render_template
from datetime import datetime, timedelta
from app.models import Photo, CalendarEvent, TimelineEvent
from app.extensions import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # 获取最新照片
    recent_photos = Photo.query.filter_by(is_private=False).order_by(Photo.uploaded_at.desc()).limit(8).all()
    
    # 获取即将到来的日历事件
    today = datetime.now().date()
    upcoming_date = today + timedelta(days=30)  # 未来30天内的事件
    upcoming_events = CalendarEvent.query.filter(
        CalendarEvent.start_time >= today,
        CalendarEvent.start_time <= upcoming_date
    ).order_by(CalendarEvent.start_time).limit(5).all()
    
    # 获取最近的时间线事件
    recent_timeline_events = TimelineEvent.query.order_by(TimelineEvent.event_date.desc()).limit(5).all()
    
    return render_template('main/index.html', 
                          current_year=datetime.now().year,
                          recent_photos=recent_photos,
                          upcoming_events=upcoming_events,
                          recent_timeline_events=recent_timeline_events)

@main.route('/about')
def about():
    return render_template('main/about.html', current_year=datetime.now().year) 