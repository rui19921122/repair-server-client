import requests
import datetime
from bs4 import BeautifulSoup
from config import is_in_rail_net


def get_repair_plan_list(start_date: datetime.date, end_date: datetime.date, session_id=None, username='', password=''):
    if not session_id:
        if len(username) == 0 or len(password) == 0:
            raise ValueError("如果未制定session_id时，则必须提供用户名和密码参数")
    url = 'http://10.128.20.119:8080/dzdxj/dzdxj/wxdxj/WxDxjHisList.faces'
    session = requests.session()
    res = session.get(url)
    res_soup = BeautifulSoup(res.text, 'lxml')
    view_state = res_soup.find('input', {'type': 'hidden', 'id': 'javax.faces.ViewState'})
    header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
              "Accept-Encoding": "gzip, deflate, sdch",
              "Accept-Language": "zh-CN,zh;q=0.8",
              "Cache-Control": "max-age=0",
              "Connection": "keep-alive",
              "Upgrade-Insecure-Requests": "1",
              "X-Requested-With": "XMLHttpRequest",
              "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 "
                            "Safari/537.36"}
    get_list_res = session.post(url,
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
    print(get_list_res.text)


if __name__ == '__main__':
    session = 'B28GZn1LMh6bZBRSSkkDn2YDPT3Jp1n4p4p2m8yHP6HPT13cv11L!-1524471908'
    f = get_repair_plan_list(datetime.date(2017, 7, 15), datetime.date(2017, 7, 16),
                             session_id='B28GZn1LMh6bZBRSSkkDn2YDPT3Jp1n4p4p2m8yHP6HPT13cv11L!-1524471908')
