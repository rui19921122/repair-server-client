import datetime

from django.db import models
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
from django.db.models import SET_NULL

from department.models import Department
import requests
from header import header
from bs4 import BeautifulSoup
import time


class Session(models.Model):
    session = models.CharField(max_length=200, verbose_name='session值')
    department = models.ForeignKey('department.Department',on_delete=SET_NULL,null=True)
    retry_nums = models.PositiveSmallIntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def login(department):
        session = requests.session()
        login_url = r'http://10.128.20.119:8080/dzdxj/login.faces'
        login_text = session.get(login_url, headers=header)
        login_text.encoding = 'utf8'
        bs_text = BeautifulSoup(login_text.text, 'lxml')
        view_state = bs_text.find('input', {'id': 'javax.faces.ViewState'})['value']
        time.sleep(1)
        res = session.post(
            login_url,
            headers=header,
            data={
                "loginForm": "loginForm",
                "loginForm:username": department.username,
                "loginForm:passwords": "",
                "loginForm:password": department.password,
                "loginForm:j_idt21": "登录",
                "javax.faces.ViewState": view_state,
            },
            allow_redirects=False
        )
        if res.status_code == 302:
            cookie = session.cookies.get('JSESSIONID')
            Session.objects.create(
                department=department,
                session=cookie
            )
        else:
            raise SystemError("login failed")
        return cookie

    @staticmethod
    def get_text(url: object, method: object, department: object, header: object, retry: object = False,
                 data: object = None,
                 need_login: object = True) -> object:
        if data is None:
            data = {
            }
        if need_login:
            try:
                if retry:
                    raise ValueError
                session_value = Session.objects.filter(department=department).latest('create_time')
                now = datetime.datetime.now()
                # 如果session已经使用了一个小时，则重置
                if (now - session_value.create_time).total_seconds() >= 3600:
                    raise ValueError
                session_value = session_value.session
                # todo 完善此处的错误捕获
            except:
                session_value = Session.login(department=department)
            session = requests.session()
            session.cookies.set(
                'JSESSIONID', session_value
            )
        else:
            session = requests
        if method == 'post':
            # 如果为post的话，需要请求viewstate,并对请求头和data进行处理
            view_state_res = session.get(
                url=url,
                headers=header
            )
            time.sleep(1)
            view_state_res.encoding = 'utf8'
            view_state_soup = BeautifulSoup(view_state_res.text, 'lxml')
            _headers = header.copy()
            _headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            _headers['Faces-Request'] = 'partial/ajax'
            _headers['X-Requested-With'] = 'XMLHttpRequest'
            if need_login:
                _headers['Cookie'] = "JSESSIONID=" + session_value
            data['javax.faces.ViewState'] = view_state_soup.find('input', {'id': 'javax.faces.ViewState'})['value'],
            header = _headers
        text = session.request(
            method=method,
            data=data,
            url=url,
            headers=header,
        )
        text.encoding = 'utf-8'
        return text.text
