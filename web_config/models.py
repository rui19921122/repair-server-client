from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class RepairCollectionsTableConfig(models.Model):
    config = models.CharField(max_length=10000)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def save(self, *args, **kwargs):
        # 每个人保存5条记录
        list = RepairCollectionsTableConfig.objects.filter(user=self.user)
        if list.count() >= 5:
            list[0].delete()
        super(RepairCollectionsTableConfig, self).save(args, kwargs)
