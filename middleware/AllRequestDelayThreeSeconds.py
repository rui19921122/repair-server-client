import time

from django.utils.deprecation import MiddlewareMixin


class AllRequestDelayThreeSeconds(MiddlewareMixin):
    def process_request(self, request):
        time.sleep(1)
        return