# encoding: utf-8
import json
import urllib
import requests
from flask import Flask, redirect, session, request, url_for, render_template, jsonify
import config
from models import db, Info, ST
from store_data import CAS_SERVER_URL, CLIENT_SERVICE_URL, CLIENT_SERVICE_PORT

app = Flask(__name__)
app.config.from_object(config)
app.config['SESSION_COOKIE_NAME'] = 'session_cas_client_' + str(CLIENT_SERVICE_PORT)
db.init_app(app)


@app.route('/')
def hello_world():
    return 'CAS Client!'


@app.route('/client/index', methods=['POST', 'GET'])
def index():
    if session.get('username') and session.get('ticket'):
        # 验证ticket是否有效
        st = ST.query.filter(ST.st == session.get('ticket'), ST.validate == 1).first()
        if st:
            # F: 展示用户信息
            username = session.get('username')
            info = Info.query.filter(Info.username == username).first()
            return render_template('index.html', data=info.info)
    if session.get('username'):
        # 清除session
        del session['username']
        del session['ticket']
    # A: 引导用户在 CAS认证中心登录
    params = {'service': CLIENT_SERVICE_URL}
    params = urllib.urlencode(params)
    url = '{}/server/login?{}'.format(CAS_SERVER_URL, params)
    return redirect(url)


@app.route('/client/service', methods=['POST', 'GET'])
def service():
    # E: 用service_ticket兑换 用户名
    service_ticket = request.args.get('ticket')
    print service_ticket
    # 记录service_ticket
    st = ST(st=service_ticket)
    db.session.add(st)
    db.session.commit()

    params = {'service': CLIENT_SERVICE_URL, 'ticket': service_ticket}
    params = urllib.urlencode(params)
    url = '{}/server/service_validate?{}'.format(CAS_SERVER_URL, params)
    resp = requests.get(url).json()
    print resp
    username = resp.get('username')
    session['username'] = username
    session['ticket'] = service_ticket
    return redirect(url_for('index'))


@app.route('/client/logout', methods=['POST', 'GET'])
def logout():
    # 用户退出：清除本地局部会话、全局会话 和 所有局部会话
    # # 清除session
    # del session['username']

    # session_id = request.cookies.get(app.session_cookie_name)
    # print session_id

    params = {'service': CLIENT_SERVICE_URL}
    params = urllib.urlencode(params)
    url = '{}/server/logout?{}'.format(CAS_SERVER_URL, params)
    return redirect(url)


@app.route('/client/close', methods=['POST'])
def close():
    # 处理CAS的通知，关闭局部会话
    service_ticket = request.json.get('ticket')
    print service_ticket
    # 注销service_ticket
    st = ST.query.filter(ST.st == service_ticket).first()
    st.validate = -1
    db.session.commit()
    return jsonify({'data': 'success'})


if __name__ == '__main__':
    app.run(port=7000)

