from .models import ScrapyPlanCacheDetail
from rest_framework import serializers


class ScrapyPlanDetailSer(serializers.ModelSerializer):
    class Meta:
        model = ScrapyPlanCacheDetail
        fields = '__all__'
        depth = 2