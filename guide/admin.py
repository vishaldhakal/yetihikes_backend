from django.contrib import admin
from .models import TravelGuide
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE

class TravelGuideAdmin(ModelAdmin):
   def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'guide_content':
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, **kwargs)


admin.site.register(TravelGuide, TravelGuideAdmin)