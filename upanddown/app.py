from flask import Flask, render_template, request, jsonify, redirect, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mongoengine import MongoEngine
from models import *
import os
import json
import random
from pathlib import Path

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_object("config")

loginmanager = LoginManager(app)
loginmanager.session_protection = "strong"
loginmanager.login_view = "login"

db = MongoEngine(app)

basedir = os.path.abspath(os.path.dirname(__file__))
download_floder = os.path.join(basedir, "upload")


def url_list(filename, name, gender, school, major, education, graduated, experience, level):
    return "<tr style='height: 45px;'><td><input type='button' id='{}' value='❌' onclick='delete_file(event)'></td>" \
           "<td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>" \
           "<td><a href='{}'><div onclick='b1_1(this)' class='b1' style='background-image: " \
           "url(/static/img/icon10.png);'></div></a></td><td><a href='javascript:;'><div onclick='b2_2(this)' " \
           "class='b2' style='background-image: url(/static/img/icon11.png);'></div></a></td><td><div class='name' " \
           "style='display: none;'>{}</div></td><td><a href='javascript:;'><div onclick='b4_4(this)' class='b4' " \
           "style='background-image: url(/static/img/icon7.png);'></div></a></div></td></tr>"\
        .format(filename, name, gender, school, major, education, graduated,
                experience, level, "/download/" + filename, current_user.nickname)


@loginmanager.user_loader
def get_user(user_id):
    return User.objects(id=user_id).first()


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main")
@login_required
def main():
    return render_template("main.html")


@app.route("/hire")
@login_required
def hire():
    return render_template("hire.html")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/error")
def error():
    return render_template("error.html")


# 上传信息
@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    elif request.method == "POST":
        err_msg = {"result": "NO"}
        param = json.loads(request.data.decode("utf-8"))
        name = param.get("name", "")
        gender = param.get("gender", "")
        school = param.get("school", "")
        major = param.get("major", "")
        education = param.get("education", "")
        graduated = param.get("graduated", "")
        experience = param.get("experience", "")
        level = param.get("level", "")
        resume = param.get("resume", "")
        interview = param.get("interview", "")
        hire = param.get("hire", "")
        if not name:
            err_msg["msg"] = "缺少姓名"
            return jsonify(err_msg)
        interviewee = Interviewee.objects(name=name)
        # 判断姓名是否重复
        if not interviewee:
            interviewee = Interviewee(name=name, gender=gender, school=school,
                                      major=major, education=education,
                                      graduated=graduated,
                                      experience=experience,
                                      level=level, resume=resume,
                                      interview=interview, hire=hire)
            interviewee.save()
            return jsonify({"result": "OK"})
        else:
            err_msg["msg"] = "简历信息已经上传"
            return jsonify(err_msg)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        err_msg = {"result": "NO"}
        param = json.loads(request.data.decode("utf-8"))
        username = param.get("username", "")
        password = param.get("password", "")
        nickname = param.get("nickname", "")
        if not username:
            err_msg["msg"] = "缺少用户名"
            return jsonify(err_msg)
        if not password:
            err_msg["msg"] = "缺少密码"
            return jsonify(err_msg)
        if not nickname:
            err_msg["msg"] = "缺少用户名"
            return jsonify(err_msg)
        user = User.objects(username=username)
        if not user:
            random_floder = random.randint(0, 10000)
            while random_floder in os.listdir(download_floder):
                random_floder = random.randint(0, 10000)
            user = User(username=username,
                        nickname=nickname,
                        floder=str(random_floder))
            user.hash_password(password)
            os.mkdir(os.path.join(download_floder, user.floder))
            print(os.path.join(download_floder, user.floder))
            return jsonify({"result": "OK"})
        else:
            err_msg["msg"] = "用户已经注册"
            return jsonify(err_msg)


@app.route("/forgot", methods=["POST", "GET"])
def forgot():
    if request.method == "GET":
        return render_template("forgot.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        err_msg = {"result": "NO"}
        param = json.loads(request.data.decode("utf-8"))
        username = param.get("username", "")
        password = param.get("password", "")
        if not username:
            err_msg["msg"] = "缺少用户名"
            return jsonify(err_msg)
        if not password:
            err_msg["msg"] = "缺少密码"
            return jsonify(err_msg)
        user = User.objects(username=username).first()
        if not user:
            err_msg["msg"] = "用户尚未注册"
            return jsonify(err_msg)
        if not user.verify_password(password):
            err_msg["msg"] = "密码错误"
            return jsonify(err_msg)
        login_user(user)
        return jsonify({"result": "OK", "next_url": "/main"})


@app.route("/upload_btn", methods=["POST"])
@login_required
def upload_btn():
    f = request.files["file"]
    if not os.path.exists(os.path.join(download_floder, current_user.floder)):
        os.mkdir(os.path.join(download_floder, current_user.floder))
    f.save(os.path.join(download_floder, current_user.floder, f.filename))
    return "上传成功"


@app.route("/get_list", methods=["GET"])
@login_required
def get_list():
    file_path = os.path.join(download_floder, current_user.floder)
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    # join拼接
    file_list = os.listdir(file_path)
    paths = sorted(file_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)), reverse=True)
    name = [n.name for n in Interviewee.objects()]
    gender = [n.gender for n in Interviewee.objects()]
    school = [n.school for n in Interviewee.objects()]
    major = [n.major for n in Interviewee.objects()]
    education = [n.education for n in Interviewee.objects()]
    graduated = [n.graduated for n in Interviewee.objects()]
    experience = [n.experience for n in Interviewee.objects()]
    level = [n.level for n in Interviewee.objects()]
    return jsonify(list(map(url_list, paths, name, gender, school, major,
                            education, graduated, experience, level)))


@app.route("/download/<string:filename>")
@login_required
def download(filename):
    if os.path.isfile(os.path.join(download_floder, current_user.floder, filename)):
        return send_from_directory(os.path.join(download_floder, current_user.floder),
                                   filename, as_attachment=True)


@app.route("/delete/<string:filename>")
@login_required
def delete_file(filename):
    if os.path.isfile(os.path.join(download_floder, current_user.floder, filename)):
        os.remove(os.path.join(download_floder, current_user.floder, filename))
        print('deleted:', filename)
        for n in Interviewee.objects():
            if n['name'] == filename.rstrip('.pdf'):
                n.delete()
        return jsonify({
            "result": "OK"
        })
    else:
        return jsonify({
            "result": "NO",
            "msg": "文件不存在"
        })


if __name__ == '__main__':
    if not os.path.exists(download_floder):
        os.makedirs(download_floder)
    app.run(host='0.0.0.0', port=5200, debug=True)
