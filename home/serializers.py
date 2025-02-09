from rest_framework import serializers
from .models import TeamMember,FeaturedTour,Testimonial,SiteConfiguration,Affiliations,Partners,TreekingNavDropdown,DestinationNavDropdown,OtherActivitiesNavDropdown,ClimbingNavDropdown,InnerDropdown,FAQ,FAQCategory,LegalDocument,GuideDropdown
from activity.serializers import NavBarActivitySmallSerializer,ActivitySmallSerializer,NavBarActivityRegionSerializer,DestinationSerializer,NavBarDestinationSerializer,NavBarActivityCategorySerializer
from guide.serializers import TravelGuideSerializer


class LegalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocument
        fields = '__all__'

class FAQCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQCategory
        fields = '__all__'

class FeaturedTourSerializer(serializers.ModelSerializer):
    featured_tours = ActivitySmallSerializer(many=True)
    popular_tours = ActivitySmallSerializer(many=True)
    best_selling_tours = ActivitySmallSerializer(many=True)
    favourite_tours = ActivitySmallSerializer(many=True)
    banner_tour = ActivitySmallSerializer(many=True)
    class Meta:
        model = FeaturedTour
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    category = FAQCategorySerializer(read_only=True)

    class Meta:
        model = FAQ
        fields = '__all__'
        
class InnerDropdownSerializer(serializers.ModelSerializer):
    activity_region = NavBarActivityRegionSerializer()
    activites = NavBarActivitySmallSerializer(many=True)

    class Meta:
        model = InnerDropdown
        fields = '__all__'

class DestinationNavDropdownSerializer(serializers.ModelSerializer):
    destinations = NavBarDestinationSerializer(many=True)

    class Meta:
        model = DestinationNavDropdown
        fields = '__all__'


class OtherActivitiesNavDropdownSerializer(serializers.ModelSerializer):
    activity_categories = NavBarActivityCategorySerializer(many=True)

    class Meta:
        model = OtherActivitiesNavDropdown
        fields = '__all__'

class ClimbingNavDropdownSerializer(serializers.ModelSerializer):
    
    innerdropdowns = InnerDropdownSerializer(many=True)

    class Meta:
        model = ClimbingNavDropdown
        fields = '__all__'

class TreekingNavDropdownSerializer(serializers.ModelSerializer):

    innerdropdowns = InnerDropdownSerializer(many=True)

    class Meta:
        model = TreekingNavDropdown
        fields = '__all__'



class SiteConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfiguration
        fields = '__all__'
        depth = 1
class AffiliationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliations
        fields = '__all__'
        depth = 2

class PartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partners
        fields = '__all__'
        depth = 2
class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'
        depth = 2

class TeamMemberSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ('id',)

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'
        depth = 2


class GuideDropdownSerializer(serializers.ModelSerializer):

    guides = TravelGuideSerializer(many=True)

    class Meta:
        model = GuideDropdown
        fields = '__all__'
        depth = 2