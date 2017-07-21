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


def get_plan_data_by_date(start: datetime.date, end: datetime.date):
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
            detail = None
            for index, item in enumerate(items):
                tds = items[index].find_all('td')
                if len(tds) >= 17:  # 确保为主项，因为合并单元格项很多数据都没有
                    if detail:
                        content_list.append(detail)
                        detail = None
                    number = tds[0].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    post_date = tds[1].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    _type = tds[2].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    direction = tds[3].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    area = tds[4].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    plan_time = tds[5].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    apply_place = tds[15].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    work_department = tds[6].find('div').find('div').get_text(strip=True)
                    work_place = tds[7].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    work_project = tds[8].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    work_detail = tds[9].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    off_power_unit = tds[10].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    work_vehicle = tds[11].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    protect_mileage = tds[12].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    on_duty_person = tds[13].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    operate_track_switch = tds[14].find('div').find('div').get_text(strip=True)
                    work_with_department = tds[16].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    extra_message = tds[17].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                    detail = {
                        'number': number,
                        'direction': direction,
                        'post_date': post_date,
                        'type': _type,
                        'plan_time': plan_time,
                        'area': area,
                        'apply_place': apply_place,
                        'content': [
                            {
                                "work_department": work_department,
                                "work_place": work_place,
                                "work_project": work_project,
                                "work_detail": work_detail,
                                "off_power_unit": off_power_unit,
                                "work_vehicle": work_vehicle,
                                "protect_mileage": protect_mileage,
                                "on_duty_person": on_duty_person,
                                "operate_track_switch": operate_track_switch,
                                "work_with_department": work_with_department,
                                "extra_message": extra_message,
                            }
                        ]
                    }
                else:
                    if detail:
                        work_department = tds[1].find('div').find('div').get_text(strip=True)
                        work_place = tds[2].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                        work_project = tds[3].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                        work_detail = tds[4].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                        off_power_unit = tds[5].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                        work_vehicle = tds[6].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                        protect_mileage = tds[7].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                        on_duty_person = tds[8].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                        operate_track_switch = tds[9].find('div').find('div').get_text(strip=True)
                        work_with_department = tds[11].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                        extra_message = tds[12].find('div').find('div').get_text('|', strip=True).split('|')[-1]
                        detail['content'].append(
                            {
                                "work_department": work_department,
                                "work_place": work_place,
                                "work_project": work_project,
                                "work_detail": work_detail,
                                "off_power_unit": off_power_unit,
                                "work_vehicle": work_vehicle,
                                "protect_mileage": protect_mileage,
                                "on_duty_person": on_duty_person,
                                "operate_track_switch": operate_track_switch,
                                "work_with_department": work_with_department,
                                "extra_message": extra_message,
                            }
                        )
                    else:
                        raise ValueError
            if detail:
                content_list.append(detail)
            return content_list

    else:
        raise ValueError()


if __name__ == '__main__':
    f = get_plan_data_by_date(datetime.date(2017, 6, 10), datetime.date(2017, 6, 12))
    print(f)
