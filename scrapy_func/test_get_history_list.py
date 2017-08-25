import unittest
from . import get_history_list
import datetime

# django环境配置
import os, sys, django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'repair_statistics_server.settings'
django.setup()


class TestGetRepairPlanList(unittest.TestCase):
    def test_func_is_ok(self):
        today = datetime.date.today()
        # 获取前三天的信息
        result = get_history_list.get_repair_plan_list(
            today - datetime.timedelta(days=3), today - datetime.timedelta(days=1), username='whdz02', password='111111'
        )
        self.assertNotEqual(len(result), 0)

        # 准备删除


if __name__ == '__main__':
    unittest.main()
