from django.contrib import admin

from contact.models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'subject', 'active', 'created']
    list_display_links = ['email']
    list_filter = ['active', 'created']
    search_fields = ['subject']
    list_editable = ['active']
    list_per_page = 10
    ordering = ('-id',)


admin.site.register(Contact, ContactAdmin)
