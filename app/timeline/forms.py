from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Length

class EventForm(FlaskForm):
    title = StringField('事件标题', validators=[
        DataRequired(message='请输入事件标题'),
        Length(min=1, max=100, message='标题长度必须在1-100个字符之间')
    ])
    description = TextAreaField('事件描述')
    date = DateField('事件日期', validators=[DataRequired(message='请选择事件日期')], format='%Y-%m-%d')
    image = FileField('事件图片', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message='只允许上传图片文件')
    ])
    submit = SubmitField('保存事件') 