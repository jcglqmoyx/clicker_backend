from django.contrib import admin

from authenticate.models import Credential, Machine

admin.site.register(Credential)
admin.site.register(Machine)