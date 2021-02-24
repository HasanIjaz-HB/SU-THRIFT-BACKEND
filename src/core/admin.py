from django.contrib import admin
# Register your models here.
from .models import product, category, ratesComments, orders


admin.site.register(product)
admin.site.register(orders)
admin.site.register(category)
admin.site.register(ratesComments)

"""
from django.contrib import admin
from django.contrib.auth.admin imçport UserAdmin
from account.models import Account


class AccountAdmin(UserAdmin):
	list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
	search_fields = ('email', 'username',)
	readonly_fields = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(Account, AccountAdmin)
"""