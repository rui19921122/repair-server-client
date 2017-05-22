import requests
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
# 因为天窗修计划的查询与登销记的查询不在一个系统中，因此这边的采用独立的Session

OPEN_PLAN_URL = 'http://10.128.20.156:8080/tcx/tcx/jhbs/jhsb_lsjhsb_info.faces'
from bs4 import BeautifulSoup

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


@api_view(['GET'])
def open_plan_scrapy_view(request,
                          start_year, start_month, start_date,
                          end_year, end_month, end_date
                          ):
    data = '''lsKfSbdate=lsKfSbdate&lsKfSbdate%3Axl=&lsKfSbdate%3AstartDate={}&lsKfSbdate%3AendDate={}&lsKfSbdate%3Aj_idt13=2100020&lsKfSbdate%3Aj_idt15=&lsKfSbdate%3Adwid=&lsKfSbdate%3Aj_idt30=&lsKfSbdate%3Aj_idt32=&lsKfSbdate%3Aj_idt37=&lsKfSbdate%3AjhsbTable%3Awi=&lsKfSbdate%3AjhsbTable%3Asi=%7C%7C%7C&javax.faces.ViewState={}&javax.faces.source=lsKfSbdate%3Aj_idt46&javax.faces.partial.event=click&javax.faces.partial.execute=lsKfSbdate%3Aj_idt46%20lsKfSbdate&javax.faces.partial.render=lsKfSbdate&javax.faces.behavior.event=click&AJAX%3AEVENTS_COUNT=1&javax.faces.partial.ajax=true'''

    session = requests.session()
    start_page = session.get(
        OPEN_PLAN_URL, headers=get_headers
    )
    if start_page.status_code == 200:
        start_page_soup = BeautifulSoup(start_page.text, 'lxml')
        view_state = start_page_soup.find('input', {'id': 'javax.faces.ViewState'})['value']
        start_date = '{}-{}-{}'.format(start_year, start_month, start_date)
        end_date = '{}-{}-{}'.format(end_year, end_month, end_date)
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
            items = text.find('tbody', {'id': 'lsKfSbdate:jhsbTable:tbn'}).find_all('tr')[3:]
            print(text)
            for index, item in enumerate(items):
                tds = items[index].find_all('td')
                if len(tds) >= 17:
                    print(tds[0].find('div').find('div').get_text())
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
            return Response(data=content_list)

    else:
        print(start_page.text)
        raise ValueError()
