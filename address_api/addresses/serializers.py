from rest_framework import serializers
from .models import Address, User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=255, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'date_joined', 'password')

    def create(self, validated_data):
         return User.objects.create_user(**validated_data)


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'address_line_1', 'address_line_2', 'city_or_town', 'country', 'postcode', 'user')

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
#         write_only_fields = ('password',)
#         read_only_fields = ('id',)
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name']
#         )
#
#         user.set_password(validated_data['password'])
#         user.save()
#
#         return user
