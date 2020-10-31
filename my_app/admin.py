from django.contrib import admin
from my_app.models import Admin_Register,Driver_Register,Tasks,Delivered,Returned,Delivery_Documents,Return_Documents,Delivery_Docs_by_admin

# Register your models here.
admin.site.register(Admin_Register)
admin.site.register(Driver_Register)
admin.site.register(Tasks)
admin.site.register(Delivered)
admin.site.register(Returned)
admin.site.register(Delivery_Documents)
admin.site.register(Return_Documents)
admin.site.register(Delivery_Docs_by_admin)
