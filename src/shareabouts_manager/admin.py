from django.contrib import admin
from django.utils.translation import ugettext as _
from shareabouts_manager.models import UserProfile, AccountOverrides, AccountPackage, CreditCard


class AccountPackageAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__str__', 'is_default')
    list_editable = ('is_default',)


class PackageOverridesInline (admin.StackedInline):
    model = AccountOverrides


class CreditCardInline (admin.StackedInline):
    model = CreditCard
    extra = 0


class UserProfileAdmin (admin.ModelAdmin):
    list_display = ('__str__', '_date_joined', 'affiliation', 'email')
    raw_id_fields = ('auth', 'package')
    inlines = [PackageOverridesInline, CreditCardInline]

    def _date_joined(self, obj):
        return obj.created_at
    _date_joined.short_description = _('Date joined')
    _date_joined.admin_order_field = 'created_at'

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(AccountPackage, AccountPackageAdmin)