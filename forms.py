from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField, TextAreaField, RadioField, DateField, FloatField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from model import *

csrf = CSRFProtect()


# 定义的表单都需要继承自FlaskFlaskForm
class LoginForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
    user_id = StringField(
        label='用户名', validators=[
            DataRequired(
                message='用户名不能为空')])
    password = PasswordField(
        label='密码', validators=[
            DataRequired(
                message='密码不能为空')])
    submit = SubmitField(label='登陆')

    def __repr__(self):
        return 'user_id: {} password: {}'.format(
            self.user_id.data, self.password.data)


class UserForm(FlaskForm):
    user_name = StringField(
        label='员工姓名', validators=[
            DataRequired(
                message='员工姓名不能为空')])
    phone = StringField(
        label='联系电话', validators=[
            DataRequired(
                message='联系电话不能为空')])
    user_password = StringField(
        label='登录密码', validators=[
            DataRequired(
                message='登录密码不能为空')])
    role = SelectField(
        label='职位',
        choices=[],
        validators=[
            DataRequired(
                message='职位不能为空')])
    birthday = DateField(
        label='出生年月')
    id_number = StringField(
        label='身份证号码', validators=[
            DataRequired(
                message='身份证号码不能为空')])

    submit = SubmitField(label='提交')

    def __init__(self):
        FlaskForm.__init__(self)
        powers = UserPowerTable.query.all()
        for power in powers:
            self.role.choices.append((power.pow_id, power.pow_name))
