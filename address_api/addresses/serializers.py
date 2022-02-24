from rest_framework import serializers
from .models import Address, User


class RegisterSerializer(serializers.ModelSerializer):
    """
    We set sure that the fields are all serialized (nice JSON format) and that the password is write-only.
    We also set a maximum and minimum length for the password to make the password is more robust.
    """

    password = serializers.CharField(max_length=30, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'date_joined', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AddressSerializer(serializers.ModelSerializer):
    """
    We make sure that the fields associated with the address are all serialized (nice JSON format)
    """
    class Meta:
        model = Address
        fields = ('id', 'address_line_1', 'address_line_2', 'city_or_town', 'country', 'postcode', 'user')


