import datetime

from bs4 import BeautifulSoup
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.decorators import api_view

from system_user.models import UserDetailInfo
from header import header

from .ser import RepairScrapyDetail, RepairScrapyHistory
from rest_framework.response import Response
from session.models import Session
import re

REPAIR_HISTORY_URL = 'http://10.128.20.119:8080/dzdxj/dzdxj/wxdxj/WxDxjHisList.faces'
REPAIR_DETAIL_URL = 'http://10.128.20.119:8080/dzdxj/dzdxj/wxdxj/continueWxDxj.faces'


# Create your views here.
@api_view(['GET'])
def scrapy_from_website_history(request,
                                start_year: str, start_month: str, start_date: str,
                                end_year: str, end_month: str, end_date: str,
                                ):
    """
    从路局需要登录的网页中爬取
    """
    url = REPAIR_HISTORY_URL
    assert isinstance(request.user, User) or isinstance(request.user, AnonymousUser)
    if request.user.is_authenticated():
        department = UserDetailInfo.objects.get(user=request.user).department
    else:
        return Response(status=403)
    text = Session.get_text(url=url,
                            method='post',
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
                                'wxdxjForm:sbDateSel1': start_year + '-' + start_month + '-' + start_date,
                                'wxdxjForm:sbDateSel2': end_year + '-' + end_month + '-' + end_date,
                            },
                            header=header,
                            department=department
                            )
    beautiful_text = BeautifulSoup(text, 'lxml')
    print(beautiful_text)
    total_nums = re.search(
        r'历史登记记录 (\d{1,4})条', text
    ).group(1)
    body = beautiful_text.find('tbody', {'id': 'wxdxjForm:dxjtable_data'})
    contents = body.find_all('tr')
    if total_nums == '0':
        raise ValueError("未解析到历史登记记录")
    else:
        total_nums = int(total_nums)
    data = [
    ]
    for content in contents:
        tds = content.find_all('td')
        cha_kan_tds = tds[7].find_all('a')
        data.append({
            'repair_type': tds[0].find('span').string,
            'repair_id': tds[1].string,
            'date': tds[2].string,
            'repair_content': tds[4].string,
            'repair_department': tds[5].string,
            'repair_login_in_area': tds[6].string,
            'inner_id': tds[7].find('a')['href'].split('?')[1],
            'repair_login_in_type': True if len(cha_kan_tds) != 1 else False
        })
        if len(contents) == total_nums:
            pass
        else:
            raise ValueError("解析到的记录数不匹配")
    return Response(
        data=RepairScrapyHistory(data, many=True).data

    )


find_time_pattern = re.compile(
    r"\(2\)\s.*?(?P<start_date>"
    r"\d{4}-\d{2}-\d{2})\s.*?(?P<start_time>\d{2}:\d{2})-"
    r"(?P<end_date>\d{4}-\d{2}-\d{2})\s.*?(?P<end_time>\d{2}:\d{2})")


@api_view(['GET'])
def scrapy_from_login_detail(request, wx_id):
    url = REPAIR_DETAIL_URL + '?wxArg=' + wx_id
    text = BeautifulSoup(Session.get_text(
        department=request.user.inner_user.department,
        url=url,
        method='get',
        header=header,
        need_login=False
    ), 'html.parser')
    tds = text.find(
        'tbody', {'id': 'wx_ydjForm:table_data'}
    ).find('tr').find_all('td')
    cheng_ren_shi_gong = tds[5]

    search_group = re.search(
        find_time_pattern,
        cheng_ren_shi_gong.find('div').find_all('div')[2].text.strip()
    )
    if not search_group:
        kai_shi_shi_jian = ''
    else:
        kai_shi_shi_jian = search_group.groups()[1]
    shi_gong_kai_tong = tds[8]
    # 此处需结合网页进行查看
    shi_gong_kai_tong_text = shi_gong_kai_tong.find('div').find_all('div')[1].text.strip()
    re_shi_gong_kai_tong_ji_hua_hao = re.search('(\d{5})', shi_gong_kai_tong_text)
    shi_gong_kai_tong_ji_hua_hao = re_shi_gong_kai_tong_ji_hua_hao.groups()[
        0] if re_shi_gong_kai_tong_ji_hua_hao else ''
    re_shi_gong_kai_tong_shi_jian = re.search('\d{4}-\d{2}-\d{2}\s*?(\d{2}:\d{2})', shi_gong_kai_tong_text)
    shi_gong_kai_tong_shi_jian = re_shi_gong_kai_tong_shi_jian.groups()[0] if re_shi_gong_kai_tong_shi_jian else ''
    try:
        ba_guan_ren = tds[9].text.split(':')[1].strip().split(' ')[0]
    except:
        ba_guan_ren = ''
    return Response(
        data=RepairScrapyDetail(
            {
                'actual_start_time': kai_shi_shi_jian,
                'actual_end_time': shi_gong_kai_tong_shi_jian,
                'actual_open_number': shi_gong_kai_tong_ji_hua_hao,
                'actual_open_person': ba_guan_ren
            }
        ).data
    )
