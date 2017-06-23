import time
from django.urls import reverse
import json

import os

# Create your tests here.
from rest_framework.test import APITestCase
from department.models import InnerUser


class TestRepairScrapyAndSaveResult(APITestCase):
    fixtures = ['data.json']

    # def test_api_detail(self):
    #     url = reverse('get_repair_data_with_detail', args=['2017', '03', '25', '2017', '03', '28'])
    #     self.client.force_login(
    #         InnerUser.objects.first().system_user
    #     )
    #     res = self.client.get(url)
    #     path = os.path.join(
    #         r'C:\Users\Administrator\Desktop\repair_system_scrapy',
    #         'data'
    #     )
    #     with open(os.path.join(path, 'global.json'), 'w') as file:
    #         json.dump(res.data, file, ensure_ascii=False)
    #     data = []
    #     for i in res.data['items']:
    #         print(i['url'])
    #         res = self.client.get(
    #             i['url']
    #         )
    #         self.assertEqual(res.status_code, 200)
    #         data.append(res.data)
    #     with open(os.path.join(path, 'good.json'), 'w') as file:
    #         json.dump(data, file, ensure_ascii=False)
    def test_api_detail(self):
        json_path = r'C:\Users\Administrator\Desktop\repair_system_scrapy\data\history.json'
        with open(json_path, 'r', encoding='utf-8') as file:
            dict = json.load(file)
        length = len(dict)
        count = 1
        for i in dict:
            url = reverse('get_repair_single_data_with_detail', args=[i['inner_id'].split('=')[-1]])
            self.client.force_login(
                InnerUser.objects.first().user
            )
            res = self.client.get(
                url
            )
            path = os.path.join(r'C:\Users\Administrator\Desktop\repair_system_scrapy\data', 'data')
            arg = i['inner_id'].split('=')[-1]
            if os.path.exists(os.path.join(path, '{}.json'.format(arg))):
                print('存在')
            else:
                with open(os.path.join(path, '{}.json'.format(arg)), 'w', encoding='utf-8') as file:
                    data = res.data
                    json.dump(data, file, ensure_ascii=False)
                    time.sleep(2)
            print('完成了{}个，共{}个'.format(count, length))
            count += 1