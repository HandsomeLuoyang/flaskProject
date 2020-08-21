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
import threading

app = Flask(__name__)
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


@app.route('/')
def hello_world():
    return 'Hello World!'


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
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# 当前实时相机画面
@app.route('/cur_camera')
def cur_camera():
    return render_template('cur_camera.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = db.session.query(UserTable).filter(
            UserTable.user_id == form.user_id.data).first()
        if not user or form.password.data != user.user_password:
            flash('用户名或密码错误')
        else:
            login_user(user)
            flash('登陆成功')
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()
