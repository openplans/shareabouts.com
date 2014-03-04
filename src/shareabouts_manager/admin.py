from django.contrib import admin
from django.utils.translation import ugettext as _
from shareabouts_manager.models import UserProfile, AccountOverrides, AccountPackage


class AccountPackageAdmin (admin.ModelAdmin):
    pass


class PackageOverridesInline (admin.StackedInline):
    model = AccountOverrides


class UserProfileAdmin (admin.ModelAdmin):
    list_display = ('__str__', '_date_joined', 'affiliation', '_email')
    raw_id_fields = ('auth', 'package')
    inlines = [PackageOverridesInline]

    def _date_joined(self, obj):
        return obj.created_at
    _date_joined.short_description = _('Date joined')
    _date_joined.admin_order_field = 'created_at'

    def _email(self, obj):
        return obj.auth.email
    _email.short_description = _('Email address')
    _email.admin_order_field = 'auth__email'

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(AccountPackage, AccountPackageAdmin)