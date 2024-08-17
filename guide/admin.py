from django.contrib import admin
from .models import GuideAuthour,TravelGuide,TravelGuideCategory,TravelGuideRegion
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE

admin.site.register(GuideAuthour, ModelAdmin)
admin.site.register(TravelGuideCategory, ModelAdmin)
admin.site.register(TravelGuideRegion, ModelAdmin)

class TravelGuideAdmin(ModelAdmin):
   def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'guide_content':
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, **kwargs)


admin.site.register(TravelGuide, TravelGuideAdmin)