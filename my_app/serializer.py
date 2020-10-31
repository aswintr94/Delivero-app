from my_app.models import Driver_Register,Tasks,Delivered,Delivery_Documents,Returned
from rest_framework import serializers

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'

class DeliveredSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivered
        fields = '__all__'

class DeliveryDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery_Documents
        fields = '__all__'

class ReturnedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Returned
        fields = '__all__'