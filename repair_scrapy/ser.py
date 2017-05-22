from rest_framework import serializers


class RepairScrapyHistory(serializers.Serializer):
    repair_type = serializers.CharField()
    repair_id = serializers.CharField()
    date = serializers.CharField()
    repair_content = serializers.CharField()
    repair_department = serializers.CharField()
    repair_login_in_area = serializers.CharField()
    inner_id = serializers.CharField()
    repair_login_in_type = serializers.BooleanField()


class RepairScrapyDetail(serializers.Serializer):
    actual_start_time = serializers.CharField()
    actual_end_time = serializers.CharField()
    actual_open_number = serializers.CharField()
    actual_open_person = serializers.CharField()
