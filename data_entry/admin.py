from django.contrib import admin

from data_entry.models import Meridian_Passage_Entry, Meridian_Passage_Sight, SunriseSunsetEntry, SightEntry, SightAlmanacEntry, StarFinderTime, StarFinderGhaAries

# Register your models here.
admin.site.register(Meridian_Passage_Entry)
admin.site.register(Meridian_Passage_Sight)
admin.site.register(SunriseSunsetEntry)
admin.site.register(SightEntry)
admin.site.register(SightAlmanacEntry)
admin.site.register(StarFinderTime)
admin.site.register(StarFinderGhaAries)