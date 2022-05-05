from rest_framework import serializers
from users.models import Hr, User
from users.helper import filter_dict

from quiz.serializer_fields import JsonListField


class UserSerializer(serializers.ModelSerializer):
    email_verified = serializers.BooleanField(read_only=True)
    phone_number_verified = serializers.BooleanField(read_only=True)
    extra_fields = JsonListField(allow_null=True)

    class Meta:
        model = User
        # fields = ['first_name', 'last_name', 'username', 'email', 'password']
        exclude = ['token', 'is_active', 'is_admin', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'roles' : {'read_only': True},
        }
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        if(self.request.user.role=='ROLE_ADMIN' and user.role == 'ROLE_HR'):
            Hr.objects.create(user=user, created_by=self.request.user)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        if(validated_data.get('password')):
            instance.set_password(validated_data['password'])
            validated_data.pop('password')
        for field in validated_data.keys():
            if(hasattr(instance, field)):
                setattr(instance, field, validated_data[field])
        instance.save()
        return instance



