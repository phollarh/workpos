from django.contrib import admin
#from django.contrib.auth.models import Group
#from .models import Profile
from .models import CustomUser,Outlets,OutletStaff,OutletStaffLogin,Profile


# Register your models here.
admin.site.register(CustomUser)
#class OutletsInline(admin.StackedInline):
#	model = Outlets
#class CustomuserAdmin(admin.ModelAdmin):
#	model= CustomUser
	#fields = [field.name for field in CustomUser._meta.get_fields()]
#	inlines =[OutletsInline]
#admin.site.unregister(CustomUser)
#admin.site.register(CustomUser, CustomuserAdmin)
admin.site.register(Outlets)
admin.site.register(OutletStaff)
admin.site.register(OutletStaffLogin)
admin.site.register(Profile)




