# django环境配置
import os
import re
import sys
import typing

import bs4
import django
import requests
from bs4 import BeautifulSoup

from scrapy_history_detail.models import PlanHistoryDetailCache

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'repair_statistics_server.settings'
django.setup()

url = 'http://10.128.20.119:8080/dzdxj/dzdxj/wxdxj/continueWxDxj.faces'
re_find_publish_number_and_time_pattern = re.compile(r'\(1\).*?(\d{3,7}).*?(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})',
                                                     re.M | re.DOTALL)
re_find_actual_time_pattern = re.compile(r'\(2\).*?(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})-\d{4}-\d{2}-\d{2} \d{2}:\d{2}',
                                         re.M | re.DOTALL)

from header import header


def get_repair_detail_by_inner_id(inner_id: str):
    detail_url = url + '?wxArg=' + inner_id
    response = requests.get(detail_url, headers=header)
    if response.status_code == 200:
        pass
    else:
        raise ConnectionError("连接失败，返回的状态码为" + response.status_code)
    soup = BeautifulSoup(response.text, 'lxml')
    tr = soup.find('tbody', {'id': 'wx_ydjForm:table_data'}).find('tr')  # 存储详情的表格
    assert isinstance(tr, bs4.element.Tag)
    tds = tr.find_all('td')  # type:typing.List[bs4.element.Tag]
    number = tds[0].get_text(strip=True)  # type:str
    repair_content = tds[1].get_text(strip=True)  # type:str
    effect_area = tds[3]. \
        find('div') \
        .find_all('div')[0] \
        .get_text(strip=True)  # type:str
    actual_start_text = tds[5] \
        .find('div') \
        .find_all('div')[2] \
        .get_text(strip=False)  # type:str
    re_result = re.search(re_find_publish_number_and_time_pattern, actual_start_text)
    try:
        publish_start_number = re_result.group(1)
        publish_start_time = re_result.group(3)
    except:
        raise ValueError("解析错误，{}".format(actual_start_text))
    actual_start_time = re.search(re_find_actual_time_pattern, actual_start_text).group(2)
    actual_end_text = tds[8] \
        .find('div') \
        .find_all('div')[1] \
        .get_text(strip=False)  # type:str
    re_end_result = re.search(re_find_publish_number_and_time_pattern, actual_end_text)
    try:
        actual_end_number = re_end_result.group(1)
        actual_end_time = re_end_result.group(3)
    except:
        raise ValueError("解析错误，{}".format(actual_end_text))
    actual_host_person = tds[9].get_text(strip=True)
    # 将采集到的数据储存在数据库中，以减轻服务器压力
    try:
        PlanHistoryDetailCache.objects.create(
            number=number,
            repair_content=repair_content,
            effect_area=effect_area,
            publish_start_time=publish_start_time,
            publish_start_number=publish_start_number,
            actual_start_time=actual_start_time,
            actual_end_time=actual_end_time,
            actual_end_number=actual_end_number,
            actual_host_person=actual_host_person,
            inner_id=inner_id
        )
    except:
        pass

    return {
        "number": number,  # 施工维修编号，格式为[JDZ]\d{3}
        "repair_content": repair_content,  # 施工项目
        "effect_area": effect_area,  # 影响使用范围
        "publish_start_time": publish_start_time,  # 命令号发布时间
        "publish_start_number": publish_start_number,  # 开始施工命令号码
        "actual_start_time": actual_start_time,  # 施工开始时间
        "actual_end_time": actual_end_time,  # 命令号结束时间
        "actual_end_number": actual_end_number,  # 开通施工命令号码
        "actual_host_person": actual_host_person,  # 把关人
    }


if __name__ == '__main__':
    pass
