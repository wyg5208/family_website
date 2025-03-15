from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class ScheduleForm(FlaskForm):
    title = StringField('日程标题', validators=[
        DataRequired(message='请输入日程标题'),
        Length(min=1, max=100, message='标题长度必须在1-100个字符之间')
    ])
    description = TextAreaField('日程描述')
    start_time = DateTimeField('开始时间', validators=[DataRequired(message='请选择开始时间')], format='%Y-%m-%d %H:%M')
    end_time = DateTimeField('结束时间', validators=[Optional()], format='%Y-%m-%d %H:%M')
    all_day = BooleanField('全天事件')
    reminder = BooleanField('需要提醒')
    reminder_time = DateTimeField('提醒时间', validators=[Optional()], format='%Y-%m-%d %H:%M')
    submit = SubmitField('保存日程')
