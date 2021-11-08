from django.contrib.auth import get_user_model
from rest_framework import serializers


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserSerializer(serializers.ModelSerializer):

    class Meta(CurrentUserSerializer.Meta):
        model = get_user_model()
        required = ('username',)
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.username)
        instance.last_name = validated_data.get('last_name', instance.username)
        instance.email = validated_data.get('email', instance.username)
        return instance


