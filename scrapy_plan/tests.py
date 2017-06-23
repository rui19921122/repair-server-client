from django.urls import reverse
from rest_framework.test import APITestCase
from department.models import Department
from system_user.models import User, UserDetailInfo
from config import is_in_rail_net
import datetime


# Create your tests here.
class TestScrapyPlan(APITestCase):
    """
    测试爬取天窗修计划的情形
    """

    def setUp(self):
        self.test_department = Department(name='测试部门', username='whdz02', password='111111')
        self.test_department.save()
        user = User.objects.create_user(
            username='test', password='111111',
            email='test@qq.com'
        )
        self.test_user = UserDetailInfo(username='测试人员',
                                        department=self.test_department,
                                        user=user)

    def test_scrapy_is_ok(self):
        """
        测试爬取是否正常,仅测试在内网的情况
        :return: 
        """
        if is_in_rail_net:
            start_date = datetime.date.today() - datetime.timedelta(days=8)
            end_date = datetime.date.today() - datetime.timedelta(days=1)
            url = reverse('查询天窗修计划历史', kwargs={
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'force_update': 'true'
            })
            self.client.force_login(self.test_user)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.body['length'], len(response.body['data']))
        else:
            return

    def test_get_data_from_cache(self):
        pass
