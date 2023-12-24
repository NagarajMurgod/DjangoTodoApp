from django.contrib import admin
from subapp.models import Account
from django.contrib.auth import get_user_model
# Register your models here.

User = get_user_model()
# print(User)
class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ('amount', 'currency')
    list_filter = ('currency',)
    search_fields = ('amount',)
    fieldsets = (
        (None, {'fields' : ('amount',)}),
        ('Currencies', {'fields' : ('currency',)})
    )

admin.site.register(Account,AccountAdmin)