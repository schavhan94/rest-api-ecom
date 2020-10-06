from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin
from django.urls import path, include
from ecom_api_app import views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register('userrole', views.UserRoleViewSet)
router.register('product', views.ProductNameViewSet)
router.register('order', views.OrderViewSet)
router.register('orderitem', views.OrderItemViewSet)
router.register('createuser', views.CreateUserView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', views.AuthToken.as_view(), name='login'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
