import datetime
import os
import sys

# django环境配置
import django
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'repair_statistics_server.settings'
django.setup()


def get_repair_plan_list(start_date: datetime.date, end_date: datetime.date, session_id=None, username='', password=''):
    # 如果配置文件为不在内网，则使用生成器返回

    if not session_id:
        if len(username) == 0 or len(password) == 0:
            raise ValueError("如果未制定session_id时，则必须提供用户名和密码参数")
    session = requests.session()
    header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
              "Accept-Encoding": "gzip, deflate, sdch",
              "Accept-Language": "zh-CN,zh;q=0.8",
              "Cache-Control": "max-age=0",
              "Connection": "keep-alive",
              "Upgrade-Insecure-Requests": "1",
              "X-Requested-With": "XMLHttpRequest",
              "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 "
                            "Safari/537.36"}
    if not session_id:
        # 如果没有提供session，则尝试登陆
        login_url = 'http://10.128.20.119:8080/dzdxj/login.faces'
        # 此登陆请求未设置header，如果日后被反爬虫了，则应设置
        get_login_res = session.get(login_url)
        if get_login_res.status_code == 200:
            soup = BeautifulSoup(get_login_res.text, 'lxml')
            login_view_state = soup.find('input', {'id': 'javax.faces.ViewState'})['value']
            try_login = session.post(login_url,
                                     headers=header,
                                     data={
                                         "loginForm": "loginForm",
                                         "loginForm:username": "whdz02",
                                         "loginForm:passwords": "",
                                         "loginForm:password": "111111",
                                         "loginForm:j_idt21": "登录",
                                         "javax.faces.ViewState": login_view_state
                                     },
                                     allow_redirects=False
                                     )
            if try_login.status_code == 302:
                pass
            else:
                raise ConnectionError("登陆失败，错误的用户名或密码？")
        else:
            raise ConnectionError("请求登陆界面失败")
    else:
        session.cookies.set('JSESSIONID', session_id)

    repair_plan_list_url = 'http://10.128.20.119:8080/dzdxj/dzdxj/wxdxj/WxDxjHisList.faces'
    res = session.get(repair_plan_list_url)
    res_soup = BeautifulSoup(res.text, 'lxml')
    view_state = res_soup.find('input', {'type': 'hidden', 'id': 'javax.faces.ViewState'})['value']
    get_list_res = session.post(repair_plan_list_url,
                                headers=header,
                                data={
                                    'javax.faces.partial.ajax': 'true',
                                    'javax.faces.partial.execute': '@all',
                                    'javax.faces.partial.render': 'wxdxjForm',
                                    'javax.faces.source': 'wxdxjForm:j_idt25',
                                    'wxdxjForm': 'wxdxjForm',
                                    'wxdxjForm:dxjtable_scrollState': '0,0',
                                    'wxdxjForm:dxjtable_selection': '',
                                    'wxdxjForm:j_idt17': '',
                                    'wxdxjForm:j_idt20': '',
                                    'wxdxjForm:j_idt23': '',
                                    'wxdxjForm:j_idt25': 'wxdxjForm:j_idt25',
                                    'wxdxjForm:sbDateSel1': start_date.strftime('%Y-%m-%d'),
                                    'wxdxjForm:sbDateSel2': end_date.strftime('%Y-%m-%d'),
                                    'javax.faces.ViewState': view_state
                                })
    if get_list_res.status_code != 200:
        raise ConnectionError("获取信息失败")
    content_soup = BeautifulSoup(get_list_res.text, 'lxml')
    list_count_soup = content_soup.find('div', {'class': 'ui-datatable-header ui-widget-header ui-corner-top'})
    list_count = list_count_soup.text[7:len(list_count_soup.text) - 3]
    try:
        list_count = int(list_count)
    except:
        raise ValueError("解析历史条目数失败")
    list_content_soup = content_soup.find('tbody', {'id': 'wxdxjForm:dxjtable_data'}).find_all('tr')
    if len(list_content_soup) != list_count:
        raise ValueError('解析到{}条数据，但网页上提供了{}条数据，条数不符合'
                         .format(len(list_content_soup), list_count))
    return_data = []
    for content_detail in list_content_soup:
        tds = content_detail.find_all('td')  # type:tds requests.
        return_data.append(
            {
                'plan_type': tds[0].text,  # 天窗修类型
                'number': tds[1].text,  # 天窗修编号
                'date': tds[2].text,  # 天窗修日期
                'plan_time': tds[3].text,  # 计划时间
                'repair_content': tds[4].text,
                'repair_department': tds[5].text,
                'apply_place': tds[6].text,
                'inner_id': tds[7].find_all('a')[0]['href'].split('=')[-1],
                'use_paper': False if len(tds[7].find_all('a')) == 1 else True,
            }
        )
    return return_data



if __name__ == '__main__':
    result = get_repair_plan_list(datetime.date(2017, 8, 1), datetime.date(2017, 8, 3),
                                  username='whdz02', password='111111'
                                  )
