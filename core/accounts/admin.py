from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User , Profile

# Register your models here.


class CustomUserAdmni(UserAdmin):
    model = User
    list_display = ("email","is_superuser","is_active","is_verified")
    list_filter = ("is_superuser","is_staff")
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        ("Personal Info" , {"fields":("email","password")}),
        ("Permissions",{"fields":("is_active","is_superuser","is_staff","is_verified")}) , 
        ("Group Permissions" , {"fields":("groups","user_permissions")}) , 
        ("Important Dates", {"fields":("last_login",)})
    )
    add_fieldsets = (
        (None , {"fields":("email","password1","password2") , "classes":["wide"]}),   
    )   

    def get_form(self, request, obj =None, **kwargs):
        form =  super().get_form(request, obj, **kwargs)
        if  not request.user.is_superuser:
            form.base_fields["is_superuser"].disabled = True
        return form


admin.site.register(Profile)
admin.site.register(User,CustomUserAdmni)