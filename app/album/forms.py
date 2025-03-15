from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, MultipleFileField
from wtforms.validators import DataRequired, Length

class AlbumForm(FlaskForm):
    title = StringField('相册标题', validators=[
        DataRequired(message='请输入相册标题'),
        Length(min=1, max=100, message='标题长度必须在1-100个字符之间')
    ])
    description = TextAreaField('相册描述')
    submit = SubmitField('保存相册')

class PhotoForm(FlaskForm):
    photos = MultipleFileField('选择照片', validators=[
        FileRequired(message='请选择至少一张照片'),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message='只允许上传图片文件')
    ])
    title = StringField('照片标题')
    description = TextAreaField('照片描述')
    is_private = BooleanField('设为私密照片')
    submit = SubmitField('上传照片') 