from django.contrib import admin
from analytics.models import Page, View, Location, Ad

admin.site.register(Location)
admin.site.register(View)
admin.site.register(Page)
admin.site.register(Ad)
