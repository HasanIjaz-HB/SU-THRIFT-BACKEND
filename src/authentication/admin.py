from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

#from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
from .models import User


class AccountAdmin(ModelAdmin):
    list_display = ('email','username', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    #search_fields = ('email', 'username', 'first_name', 'last_name')
    #readonly_fields = ('date_joined', 'last_login')

    #filter_horizantol = ()
    #list_filter = ()
    #fieldsets = ()

admin.site.register(User, AccountAdmin)
#admin.site.register(product)
#admin.site.register(category)
#admin.site.register(ratesComments)