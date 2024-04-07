from rest_framework import serializers

from materials.serializer import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(source='payment_set', read_only=True, many=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'city', 'phone', 'avatar', 'payment', 'password']
