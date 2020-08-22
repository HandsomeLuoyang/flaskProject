from flask import Flask, render_template, request, make_response, jsonify, flash, url_for, redirect, Response
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from log import login_log, fire_log
from role import *
from model import *
from exts import db, Config
from forms import *
from sqlalchemy import and_, extract
import re
import traceback
import datetime
from camera import *
import os

app = Flask(__name__, static_url_path='')
login_manager = LoginManager()

app.config.from_object(Config)
# 初始化
db.init_app(app)
csrf.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

video_camera = VideoCamera()
video_camera.start_record()


@login_manager.user_loader
def load_user(userid):
    return db.session.query(UserTable).get(userid)


# 历史视频查看
@app.route('/history_video')
@login_required
def history_video():
    date = request.args.get('date', '2020-07-01')
    src = 'mp4/if_you.mp4'
    return jsonify(src=src)


@app.route('/jquery')
def asdawqe():
    return render_template('jQuery_test.html')


# 用户列表
@app.route('/user_list')
@admin_required
@login_required
def user_list():
    all_user = db.session.query(UserTable).all()
    for i in all_user:
        print(i)
    return render_template('user_list.html', all_user=all_user)


@app.route('/add_user', methods=['GET', 'POST'])
@admin_required
@login_required
def add_user():
    form = UserForm()
    if request.method == 'POST':
        print(form.user_name.data)
        print(form.role.data)
        print(form.phone.data)
        user_item = UserTable(user_id=0, pow_id=form.role.data, user_name=form.user_name.data, user_password=form.user_password.data,
                              phone_number=''.join(form.phone.data.split(' ')), birthday=form.birthday.data, id_card=form.id_number.data)
        db.session.add(user_item)
        db.session.commit()

    return render_template('add_user.html', form=form)

# 监控列表页面
@app.route('/monitor')
@login_required
def monitor():
    return render_template("monitor.html")

# 监控详情页面
@app.route('/monitor_details')
@login_required
def monitor_details():
    return render_template("monitor_details.html")


@csrf.exempt
@app.route('/test', methods=['POST', 'GET'])
def test():

    # print(request.values['time'])

    return render_template('admin_index.html')


@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.pow.pow_id == 1:
        return render_template('admin_index.html')
    else:
        return render_template('common_index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# 相机推流
def gen(camera):
    # for frame in camera.get_frame():
    #     yield (b'--frame\r\n'
    #            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    while True:
        frame = video_camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# 相机喂流
@app.route('/video_feed')
@login_required
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# 当前实时相机画面
@app.route('/cur_camera')
@login_required
def cur_camera():
    return render_template('cur_camera.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = db.session.query(UserTable).filter(
            UserTable.user_name == form.user_id.data).first()
        if not user or not user.verify_password(form.password.data):
            flash('用户名或密码错误')
            login_log.info(
                '用户名:{} 尝试登录 登录失败！！'.format(
                    form.user_id.data,
                    form.password))
        else:
            login_user(user)
            flash('登陆成功')
            login_log.info('用户名:{} 登录成功！！'.format(form.user_id.data))
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()
