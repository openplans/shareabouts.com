from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ugettext as _
from shareabouts_manager.models import UserProfile, AccountOverrides, AccountPackage, CreditCard


class AccountPackageAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__str__', 'is_default')
    list_editable = ('is_default',)


    def get_queryset(self, request):
        qs = super(AccountPackageAdmin, self).get_queryset(request)

        # If this is not a simple GET request, just return the base queryset
        # immediately.
        if request.method.lower() != 'get':
            return qs

        # Otherwise, calculate the number of packages with is_default and show
        # a message if necessary
        total_count = qs.count()
        is_default_count = qs.filter(is_default=True).count()

        if total_count == 0:
            self.message_user(
                request, "You must have at least one account package!",
                level=messages.ERROR)
        elif is_default_count == 0:
            self.message_user(
                request, "There is no default package selected! You must "
                         "select a default package.",
                level=messages.ERROR)
        elif is_default_count > 1:
            self.message_user(
                request, "You have more than one package selected as default. "
                         "Only one package should be default.",
                level=messages.ERROR)

        return qs


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