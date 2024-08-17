from django.contrib import admin
from .models import TeamMember,Testimonial,LegalDocument,FeaturedTour,Affiliations,SiteConfiguration,Partners,TreekingNavDropdown,DestinationNavDropdown,OtherActivitiesNavDropdown,ClimbingNavDropdown,InnerDropdown,FAQ,FAQCategory,NewsletterSubscription
from solo.admin import SingletonModelAdmin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, ModelAdmin)
admin.site.register(Group, ModelAdmin)

class UnfoldSingletonModelAdmin(SingletonModelAdmin, ModelAdmin):
    pass


admin.site.register(SiteConfiguration, UnfoldSingletonModelAdmin)
admin.site.register(FeaturedTour, UnfoldSingletonModelAdmin)
admin.site.register(DestinationNavDropdown, UnfoldSingletonModelAdmin)
admin.site.register(ClimbingNavDropdown, UnfoldSingletonModelAdmin)
admin.site.register(OtherActivitiesNavDropdown, UnfoldSingletonModelAdmin)
admin.site.register(TreekingNavDropdown, UnfoldSingletonModelAdmin)
admin.site.register(InnerDropdown,ModelAdmin)
admin.site.register(Affiliations,ModelAdmin)
admin.site.register(Partners,ModelAdmin)
admin.site.register(FAQ,ModelAdmin)
admin.site.register(FAQCategory,ModelAdmin)
admin.site.register(Testimonial,ModelAdmin)
admin.site.register(LegalDocument,ModelAdmin)
admin.site.register(NewsletterSubscription,ModelAdmin)


class TeamMemberAdmin(ModelAdmin):
   def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'about':
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, **kwargs)

admin.site.register(TeamMember,TeamMemberAdmin)