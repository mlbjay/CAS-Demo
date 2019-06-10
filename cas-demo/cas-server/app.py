# encoding: utf-8
import urllib
import uuid

from flask import Flask, request, render_template, redirect, url_for, make_response, jsonify
import config
from main import create_tgt, create_st, notify_clients
from models import db, User, TGT, ST, Service

app = Flask(__name__)
app.config.from_object(config)
app.config['SESSION_COOKIE_NAME'] = 'session_cas_server'
db.init_app(app)


@app.route('/')
def hello_world():
    return 'CAS Server!'


@app.route('/server/login', methods=['POST', 'GET'])
def login():
    # 在认证中心登录
    if request.method == 'GET':
        # 获取GASTGC，查找TGT是否存在
        castgc = request.cookies.get('CASTGC')
        print castgc
        if castgc:
            tgt = TGT.query.filter(TGT.id == int(castgc), TGT.validate == 1).first()
            if tgt:
                # TGT存在，证明 用户已登录
                # 签发 service_ticket
                url = create_st(tgt.user_id, tgt.id)
                if url:
                    return redirect(url)
                else:
                    return 'no service & login success'
        return render_template('login.html')
    else:
        # B: 登录
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username==username, User.password==password).first()
        if user:
            # TGT不存在，证明 用户未登录
            # C: 生成 TGT，ticket_granted_ticket
            tgc = create_tgt(user.id)
            print tgc
            # 签发 service_ticket
            url = create_st(user.id, tgc)
            if url:
                # D: 重定向回到 client
                # 保存TGC在cookie
                response = redirect(url)
                response.set_cookie('CASTGC', str(tgc))
                return response
            else:
                response = make_response('no service & login success')
                response.set_cookie('CASTGC', str(tgc))
                return response
        else:
            return u'用户名或者密码错误'


@app.route('/server/service_validate', methods=['POST', 'GET'])
def validate():
    # E: 验证service_ticket
    service_ticket = request.args.get('ticket')
    service_url = request.args.get('service')
    print service_ticket
    service = Service.query.filter(Service.url == service_url).first()
    st = ST.query.filter(ST.st == service_ticket,
                         ST.service_id == service.id,
                         ST.used == 0, ST.validate == 1).first()
    if st:
        user = User.query.filter(User.id == st.user_id).first()
        print user.username
        # service_ticket只能使用一次
        st.used += 1
        db.session.commit()
        # 用json格式 代替 xml文件
        return jsonify({'username': user.username})
    return 'check'


@app.route('/server/logout', methods=['POST', 'GET'])
def logout():
    service = request.args.get('service')
    print service
    # 用CASTGC查找ST
    castgc = request.cookies.get('CASTGC')
    tgt = TGT.query.filter(TGT.id == int(castgc)).first()
    st_models = ST.query.filter(ST.tgt_id == tgt.id, ST.validate == 1).all()
    for model in st_models:
        notify_clients(model)

    response = make_response('CAS server logout')
    # 注销CASTGC
    response.delete_cookie('CASTGC')
    return response


if __name__ == '__main__':
    app.run(port=7432)

