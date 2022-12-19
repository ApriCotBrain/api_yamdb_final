from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from users.models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'bio',
            'role',
            'last_name',
            'first_name',
        )


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]
    list_display = (
        'username',
        'email'
    )
