from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    albums = db.relationship('Album', backref='owner', lazy='dynamic')
    events = db.relationship('Event', backref='owner', lazy='dynamic')
    schedules = db.relationship('Schedule', backref='owner', lazy='dynamic')
    timeline_events = db.relationship('TimelineEvent', backref='owner', lazy='dynamic')
    calendar_events = db.relationship('CalendarEvent', backref='owner', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cover_photo_id = db.Column(db.Integer, nullable=True)
    photos = db.relationship('Photo', backref='album', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Album {self.title}>'
    
    @property
    def cover_photo(self):
        if self.cover_photo_id:
            return Photo.query.get(self.cover_photo_id)
        return None

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    is_private = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Photo {self.filename}>'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, index=True, nullable=False)
    image = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id], overlaps="events,owner")
    
    def __repr__(self):
        return f'<Event {self.title}>'

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, index=True, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    all_day = db.Column(db.Boolean, default=False)
    reminder = db.Column(db.Boolean, default=False)
    reminder_time = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id], overlaps="schedules,owner")
    
    def __repr__(self):
        return f'<Schedule {self.title}>'

class TimelineEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, index=True, nullable=False)
    location = db.Column(db.String(100))
    photo_filename = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id], overlaps="timeline_events,owner")
    
    def __repr__(self):
        return f'<TimelineEvent {self.title}>'

class CalendarEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, index=True, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    all_day = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(100))
    category = db.Column(db.String(20), default='other')  # birthday, anniversary, holiday, appointment, other
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id], overlaps="calendar_events,owner")
    
    def __repr__(self):
        return f'<CalendarEvent {self.title}>'

class Carousel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(100))
    order = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id], overlaps="owner")
    
    def __repr__(self):
        return f'<Carousel {self.title}>'