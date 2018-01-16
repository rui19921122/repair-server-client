# 从路局天窗修计划中读取历史内容
import requests
from bs4 import BeautifulSoup
import datetime

OPEN_PLAN_URL = 'http://10.128.20.156:8080/tcx/tcx/jhbs/jhsb_lsjhsb_info.faces'
get_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip,deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "10.128.20.156:8080",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 " \
                  "Safari/537.36",
}

post_headers = {
    "Host": "10.128.20.156:8080",
    "Connection": "keep-alive",
    "Faces-Request": "partial/ajax",
    "Origin": "http://10.128.20.156:8080",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 "
                  "Safari/537.36",
    "Content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
}


def get_repair_plan_data_by_date(start: datetime.date, end: datetime.date):
    session = requests.session()
    data = '''lsKfSbdate=lsKfSbdate&lsKfSbdate%3Axl=&lsKfSbdate%3AstartDate={}&lsKfSbdate%3AendDate={}&lsKfSbdate%3Aj_idt13=2100020&lsKfSbdate%3Aj_idt15=&lsKfSbdate%3Adwid=&lsKfSbdate%3Aj_idt30=&lsKfSbdate%3Aj_idt32=&lsKfSbdate%3Aj_idt37=&lsKfSbdate%3AjhsbTable%3Awi=&lsKfSbdate%3AjhsbTable%3Asi=%7C%7C%7C&javax.faces.ViewState={}&javax.faces.source=lsKfSbdate%3Aj_idt46&javax.faces.partial.event=click&javax.faces.partial.execute=lsKfSbdate%3Aj_idt46%20lsKfSbdate&javax.faces.partial.render=lsKfSbdate&javax.faces.behavior.event=click&AJAX%3AEVENTS_COUNT=1&javax.faces.partial.ajax=true'''
    start_page = session.get(
        OPEN_PLAN_URL, headers=get_headers
    )
    if start_page.status_code == 200:
        start_page_soup = BeautifulSoup(start_page.text, 'html.parser')
        view_state = start_page_soup.find('input', {'id': 'javax.faces.ViewState'})['value']
        start_date = '{}-{}-{}'.format(start.year, start.month, start.day)
        end_date = '{}-{}-{}'.format(end.year, end.month, end.day)
        data = data.format(
            start_date, end_date, view_state
        )
        used_post_headers = post_headers.copy()
        used_post_headers['Referer'] = "http://10.128.20.156:8080/tcx/tcx/jhbs/jhsb_lsjhsb_info.faces"
        res = session.post(
            OPEN_PLAN_URL, data=data, headers=post_headers
        )
        if res.status_code == 200:
            text = BeautifulSoup(res.text, 'lxml')
            content_list = []
            try:
                items = text.find('tbody', {'id': 'lsKfSbdate:jhsbTable:tbn'}).find_all('tr')[3:]
            except AttributeError:
                raise ValueError('没有发现任何数据')
            for index, item in enumerate(items):
                tds = items[index].find_all('td')
                if len(tds) >= 17:  # 确保为主项，因为合并单元格项很多数据都没有
                    repair_id = tds[0].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    repair_date = tds[1].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    repair_type = tds[2].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    repair_area = tds[4].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    repair_time = tds[5].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    content_list.append(
                        {
                            'repair_id': repair_id,
                            'repair_date': repair_date,
                            'repair_type': repair_type,
                            'repair_time': repair_time,
                        }
                    )
            return content_list

    else:
        raise ValueError()


if __name__ == '__main__':
    f = get_repair_plan_data_by_date(datetime.date(2017, 6, 10), datetime.date(2017, 6, 12))
