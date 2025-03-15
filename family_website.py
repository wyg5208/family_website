from app import create_app, db
from app.models import User, Album, Photo, Event, Schedule, TimelineEvent, CalendarEvent

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Album': Album, 
        'Photo': Photo, 
        'Event': Event, 
        'Schedule': Schedule,
        'TimelineEvent': TimelineEvent,
        'CalendarEvent': CalendarEvent
    }

if __name__ == '__main__':
    app.run(debug=True) 