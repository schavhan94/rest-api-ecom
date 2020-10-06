from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (UserRole, UserProfile, ProductName, Order, OrderItem,)

# Register your models here.


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ["id", "title", ]


admin.site.register(UserRole, UserRoleAdmin)


class UserAdmin(admin.ModelAdmin):
     list_display = ["id", "email", "is_active", "userrole"]

admin.site.register(UserProfile, UserAdmin)


class ProductNameAdmin(admin.ModelAdmin):
    list_display = ["id", "product_name", "price", "vender"]


admin.site.register(ProductName, ProductNameAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "order_status", "order_item", "vender"]


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "productname", "quantity"]


admin.site.register(OrderItem, OrderItemAdmin)
