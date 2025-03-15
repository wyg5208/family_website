from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Optional

class CarouselForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('描述', validators=[Optional(), Length(max=500)])
    image = FileField('图片', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '只允许上传图片文件！')
    ])
    order = IntegerField('排序', validators=[Optional()], default=0)
    active = BooleanField('启用', default=True)
    submit = SubmitField('保存')

class CarouselEditForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('描述', validators=[Optional(), Length(max=500)])
    image = FileField('图片', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '只允许上传图片文件！')
    ])
    order = IntegerField('排序', validators=[Optional()], default=0)
    active = BooleanField('启用', default=True)
    submit = SubmitField('保存') 