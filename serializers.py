from rest_framework import serializers
from django.utils import timezone
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    time_remaining_minutes = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_time_remaining_minutes(self,obj):
        elapsed = timezone.now() - obj.created_at
        total_sla_seconds =  obj.sla_hours*3600
        remaining_seconds = total_sla_seconds - elapsed.total_seconds()
        return round(remaining_seconds/60,1)