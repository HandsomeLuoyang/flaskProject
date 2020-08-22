from flask import Flask, render_template, request, make_response, jsonify, flash, url_for, redirect, Response
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
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


# jQuery测试
@app.route('/jquery_test')
def jquery():
    # a = request.args.get('a',0,type=int)
    # b = request.args.get('b',0,type=int)
    src = 'mp4/love.mp4'
    return jsonify(src=src)
    return render_template('jQuery_test.html')


# 历史视频查看
@app.route('/history_video')
def history_video():
    date = request.args.get('date', '2020-07-01')
    src = 'mp4/if_you.mp4'
    return jsonify(src=src)


@app.route('/jquery')
def asdawqe():
    admin = UserTable(0, 1,'admin', 'admin', '123123', '2000-01-01', '430528xxxxxx')
    db.session.add(admin)
    db.session.commit()
    return render_template('jQuery_test.html')

# 用户列表
@app.route('/user_list')
def user_list():
    return render_template('user_list.html')


@app.route('/add_user')
def add_user():
    return render_template('add_user.html')

# 监控列表页面
@app.route('/monitor')
def monitor():
    return render_template("monitor.html")

# 监控详情页面
@app.route('/monitor_details')
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
    return render_template('admin_index.html')


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
        else:
            login_user(user)
            flash('登陆成功')
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()
