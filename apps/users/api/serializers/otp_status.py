from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from user.models import OTPStatus


class OTPStatusSerializer(serializers.Serializer):
    message_id = serializers.CharField()
    user_sms_id = serializers.CharField()
    country = serializers.CharField()
    phone_number = PhoneNumberField()
    sms_count = serializers.IntegerField()
    status = serializers.CharField()
    status_date = serializers.DateTimeField()

    def create(self, validated_data):
        instance, _ = OTPStatus.objects.get_or_create(user_sms_id=validated_data.get('user_sms_id'))
        instance.message_id = validated_data.get('message_id')
        instance.status = validated_data.get('status')
        instance.status_date = validated_data.get('status_date')
        instance.country = validated_data.get('country')
        instance.phone = validated_data.get('phone_number')
        instance.sms_count = validated_data.get('sms_count')
        instance.save()
        return instance
