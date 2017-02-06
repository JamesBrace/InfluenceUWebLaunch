
from rest_framework import serializers
from django.contrib.auth import update_session_auth_hash


from verification.models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ('id', 'email', 'created_at', 'updated_at', 'first_name', 'last_name', 'password', 'confirm_password')
        read_only_fields = ('created_at', 'updated_at',)

        def create(self, validated_data):
            return Account.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.username = validated_data.get('email', instance.email)
            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password:
                if password == confirm_password:
                    instance.set_password(password)
                    instance.save()
                else:
                    raise serializers.ValidationError({"password": ["Passwords don't match."]})

            update_session_auth_hash(self.context.get('request'), instance)

            return instance

class ResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=40)
    last_name = serializers.CharField(max_length=40)
