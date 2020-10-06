from django.db.models import fields
from .models import (UserRole, UserProfile, ProductName, Order, OrderItem)
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class UserRoleSerializer(ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'
        read_only_fields = ['id']


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "first_name", "last_name",
                  "email", "userrole", "password", "is_active"]
        read_only_fields = ['id']

        extra_kwargs = {
            'password': {
                'write_only': True,
            },
            'style': {
                'input_type': 'password',
            }
        }

    def create(self, validated_data):
        email = validated_data.get('email')
        is_email_present = UserProfile.objects.filter(email=email)
        if is_email_present:
            raise serializers.ValidationError('User already register...')

        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        userrole = validated_data.get('userrole')
        password = validated_data.get('password')
        is_active = validated_data.get('is_active', True)

        user = UserProfile(
            email=email,
            first_name=first_name,
            last_name=last_name,
            userrole=userrole,
            password=password,
            is_active=is_active
        )
        user.set_password(password)
        user.save()
        return user


class ProductNameSerializer(ModelSerializer):
    class Meta:
        model = ProductName
        exclude = ['vender', ]
        read_only_fields = ['id']

    def create(self, validated_data):
        user = validated_data.get('vender')
        print('*'*100)
        print(user.userrole)
        if user.userrole.title == 'Vendor':
            user = ProductName.objects.create(**validated_data)
            user.save()
            return user
        else:
            raise serializers.ValidationError(
                {'details': 'Only vendor can add product'})


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ['id', 'price']

    def create(self, validated_data):
        price = validated_data.get('productname').price
        quantity = validated_data.get('quantity')
        productname = validated_data.get('productname')

        vender = validated_data.get('productname').vender
        customer = validated_data.get('user')

        order_item_obj = OrderItem(
            price=price, quantity=quantity, productname=productname)
        order_item_obj.save()

        order_obj = Order(order_item=order_item_obj,
                          user=customer, vender=vender)
        order_obj.save()

        return order_item_obj


class OrderSerializer(ModelSerializer):
    order_item = OrderItemSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'user', 'vender']
