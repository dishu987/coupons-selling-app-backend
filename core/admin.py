from django.contrib import admin
from .models import UserModel,CouponModel,OTPModel,Message,Conversation


admin.site.register(UserModel)
admin.site.register(CouponModel)
admin.site.register(OTPModel)
admin.site.register(Conversation)
admin.site.register(Message)