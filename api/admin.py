from django.contrib import admin
from api.models import *

# Register your models here.

class ClientFileInline(admin.TabularInline):
   model = File
   extra = 1

class ClientAdmin(admin.ModelAdmin):
    inlines = [ClientFileInline]

admin.site.register(Client, ClientAdmin)
admin.site.register(File)
# admin.site.register(ClientFile)


# @admin.register(ClientFile)
# class ClientFileAdmin(admin.ModelAdmin):
#     list_display = ('id', 'mom')

# @admin.register(Client)
# class ClientAdmin(admin.ModelAdmin):
#     # Use filter_horizontal to allow selecting multiple ClientFile instances
#     filter_horizontal = ('mom',)
#     # list_display = ('id', 'client_name', 'entity_type')

# admin.site.register(Client)
# admin.site.register(File)
# admin.site.register(User)
# admin.site.register(Branch)
# admin.site.register(OfficeLocation)
# admin.site.register(Customer)
# admin.site.register(HSNCode)
# admin.site.register(SalesInvoice)
# admin.site.register(PurchaseInvoice)
# admin.site.register(BranchDocument)
# admin.site.register(CompanyDocument)
