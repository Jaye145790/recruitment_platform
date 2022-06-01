from flask import Flask, render_template, request, jsonify, redirect, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mongoengine import MongoEngine
from models import *
import os
import json
import random
from pathlib import Path
from distutils.util import  strtobool
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_object("config")

loginmanager = LoginManager(app)
loginmanager.session_protection = "strong"
loginmanager.login_view = "login"

db = MongoEngine(app)

basedir = os.path.abspath(os.path.dirname(__file__))
download_floder = os.path.join(basedir, "upload")


# icon10是简历按钮、icon11是面试按钮、icon7是录用按钮
def url_list(id, filename, name, gender, school, major, education, graduated, experience, level, resume, interview, hire,dept,thinkDate):
    res = "<tr style='height: 45px;' id='{}'><td><input type='button' id='{}' value='❌' onclick='delete_file(event)'></td>" \
           "<td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>" \
           "<td><a href='{}'><div onclick='b1_1(this)' name='resume' class='b1' style='background-image: " \
           "url(/static/img/iconOne.png);'></div></a></td><td><a href='javascript:;'><div onclick='b2_2(this)' name='interview' " \
           "class='b2' style='background-image: url(/static/img/iconTwo.png);'></div></a></td><td><div name='dept'>{}</div> " \
           "</td><td><a href='javascript:;'><div onclick='b4_4(this)' name='hire' class='b4' " \
           "style='background-image: url(/static/img/iconThree.png);' value='{}'></div></a></div></td></tr>"\
        .format(id, filename, name, gender, school, major, education, graduated,
                experience, level, "/download/" + filename, dept,thinkDate)
    print(resume,interview)
    if resume:
        res = res.replace('iconOne', 'icon10')
    else:
        res = res.replace('iconOne', 'icon5')
    if interview:
        res = res.replace('iconTwo', 'icon11')
    else:
        res = res.replace('iconTwo', 'icon6')
    if hire:
        res = res.replace('iconThree', 'icon9')
    else:
        res = res.replace('iconThree', 'icon7')
    return res


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


@app.route("/changepassword", methods=["POST", "GET"])
def changepassword():
    return render_template("changepassword.html")


@app.route("/changesuccess")
def changesuccess():
    return render_template("changesuccess.html")


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
                                      level=level,)
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
            # random_floder = random.randint(0, 10000)
            # while random_floder in os.listdir(download_floder):
            #     random_floder = random.randint(0, 10000)
            user = User(username=username,
                        nickname=nickname,
                        floder=str(4125))
            user.hash_password(password)
            # os.mkdir(os.path.join(download_floder, user.floder))
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
    id = [n.id for n in Interviewee.objects()]
    gender = [n.gender for n in Interviewee.objects()]
    school = [n.school for n in Interviewee.objects()]
    major = [n.major for n in Interviewee.objects()]
    education = [n.education for n in Interviewee.objects()]
    graduated = [n.graduated for n in Interviewee.objects()]
    experience = [n.experience for n in Interviewee.objects()]
    level = [n.level for n in Interviewee.objects()]
    resume = [n.resume for n in Interviewee.objects()]
    interview = [n.interview for n in Interviewee.objects()]
    hire = [n.hire for n in Interviewee.objects()]
    thinkDate = [n.thinkDate for n in Interviewee.objects()]
    dept = [n.dept for n in Interviewee.objects()]
    return jsonify(list(map(url_list, id,paths, name, gender, school, major,
                            education, graduated, experience, level,resume,interview,hire,dept,thinkDate)))


@app.route("/download/<string:filename>")
@login_required
def download(filename):
    if os.path.isfile(os.path.join(download_floder, current_user.floder, filename)):
        return send_from_directory(os.path.join(download_floder, current_user.floder),
                                   filename, as_attachment=True)
#　更改用户信息与简历功能
@app.route("/update_user/",methods=["POST"])
@login_required
def update_user():
    if request.method == 'POST':
        data = request.form
        print('update_user',data)
        Interviewee.objects(id=data['user_id']).update(thinkDate=data['thinkDate'],dept=data['dept'], resume=data['resume']=='true',interview=data['interview']=='true',hire=data['hire']=='true')
        return 'OK'
# 删除用户信息与简历功能
@app.route("/delete_user/",methods=["POST"])
@login_required
def delete_user():
    if request.method=='POST':
        param = request.form
        filename = param.get("filename", "")
        user_id = param.get("user_id", "")
        #删除对应用户信息
        Interviewee.objects(id=user_id).delete()
        #删除对应简历文件
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
    app.run(host='0.0.0.0', port=5000, debug=True)
