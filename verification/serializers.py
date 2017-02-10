from rest_framework import serializers

from verification.models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ('id', 'email', 'created_at', 'updated_at', 'full_name', 'password')
        read_only_fields = ('created_at', 'updated_at',)

        def create(self, validated_data):
            return Account.objects.create(**validated_data)


class ResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=40)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=40)
    special_key = serializers.CharField(max_length=40)


class UpdateSerializer(serializers.Serializer):
    option = serializers.CharField(max_length=15)
    phone = serializers.CharField(max_length=15)
    size = serializers.CharField(max_length=5)
    country = serializers.CharField(max_length=3)
    gender = serializers.CharField(max_length=2)
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=40, required=False)
    special_key = serializers.CharField(max_length=40, required=False)
