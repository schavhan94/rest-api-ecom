from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (UserRole, UserProfile, ProductName, Order, OrderItem,)

# Register your models here.


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ["id", "title", ]


admin.site.register(UserRole, UserRoleAdmin)


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        # (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_active', 'is_staff', 'userrole'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name',
                    'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('first_name',)
    filter_horizontal = ('groups', 'user_permissions',)


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
