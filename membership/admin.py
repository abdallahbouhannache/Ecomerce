# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Membership
from membership.models import Member

admin.site.unregister(User)
# Register your models here.
class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    verbose_name_plural = 'Member'
    fk_name = 'user'

 
class MemberAdmin(UserAdmin):
    inlines = (MemberInline, )

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(User, MemberAdmin)