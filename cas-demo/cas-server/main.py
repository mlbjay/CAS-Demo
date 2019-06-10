# encoding: utf-8
import json
import urllib
import uuid
from flask import request
import requests

from models import TGT, db, ST, Service


def create_tgt(user_id):
    """生成 TGT"""
    tgt_model = TGT(tgt=str(uuid.uuid1()), user_id=user_id)
    db.session.add(tgt_model)
    db.session.commit()
    return tgt_model.id


def create_st(user_id, tgt_id):
    """生成 ST"""
    service_url = request.args.get('service')
    # 验证service是否已注册
    service = Service.query.filter(Service.url == service_url).first()
    if service_url and service:
        st_model = ST(st=str(uuid.uuid1()),
                      user_id=user_id,
                      tgt_id=tgt_id,
                      url=service_url,
                      service_id=service.id,
                      used=0)
        db.session.add(st_model)
        db.session.commit()
        # 签发 service_ticket
        params = {'ticket': st_model.st}
        params = urllib.urlencode(params)
        url = '{}?{}'.format(service_url, params)
        return url
    else:
        return None


def notify_clients(st):
    print st.service_id
    service = Service.query.filter(Service.id == st.service_id).first()
    print service.logout_url
    # 注销service_ticket
    st.validate = -1
    db.session.commit()
    # 发出 service_ticket
    data = {'ticket': st.st}
    # fire and forget
    resp = requests.post(service.logout_url,
                         data=json.dumps(data),
                         verify=False, timeout=0.1,
                         headers={'Content-Type': 'application/json'})
    print resp.json()
    return None




