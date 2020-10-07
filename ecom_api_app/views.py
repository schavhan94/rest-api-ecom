from rest_framework.response import Response
from ecom_api_app import serializers
from rest_framework import viewsets
from ecom_api_app.models import (
    UserRole, UserProfile, ProductName, Order, OrderItem)
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
    RetrieveModelMixin, UpdateModelMixin,ListModelMixin)


class UserRoleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserRoleSerializer
    queryset = UserRole.objects.all()


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()


class ProductNameViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductNameSerializer
    queryset = ProductName.objects.all()

    def perform_create(self, serializer):
        serializer.save(vender=self.request.user)


class OrderViewSet(ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()


class OrderItemViewSet(ListModelMixin,
                       CreateModelMixin,
                       DestroyModelMixin,
                       RetrieveModelMixin,
                       GenericViewSet):

    serializer_class = serializers.OrderItemSerializer
    queryset = OrderItem.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AuthToken(ObtainAuthToken):
    '''Generating Custom Auth Token'''

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        return Response({'msg': 'invalid credentials'}, status=403)

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CreateUserView(CreateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = []

class ApiRoot(ListModelMixin, GenericViewSet):
    permission_classes = [AllowAny, ]
    authentication_classes = []
    def list(self, request, *args, **kwargs):
        print('hiii')
        return Response({"userrole": "https://restmagic.herokuapp.com/userrole/",
                        "product": "https://restmagic.herokuapp.com/product/",
                        "order": "https://restmagic.herokuapp.com/order/",
                        "orderitem": "https://restmagic.herokuapp.com/orderitem/",
                        "createuser": "https://restmagic.herokuapp.com/createuser/"})