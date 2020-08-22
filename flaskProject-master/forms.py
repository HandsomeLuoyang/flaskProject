from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField, TextAreaField, RadioField, \
    DateField, FloatField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from model import *

csrf = CSRFProtect()


# 定义的表单都需要继承自FlaskFlaskForm
class LoginForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
    user_id = StringField(label='用户名', validators=[DataRequired(message='用户名不能为空')])
    password = PasswordField(label='密码', validators=[DataRequired(message='密码不能为空')])
    submit = SubmitField(label='登陆')

    def __repr__(self):
        return 'user_id: {} password: {}'.format(self.user_id.data, self.password.data)
