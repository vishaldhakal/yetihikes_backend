from rest_framework import serializers
from .models import TravelGuide
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup

class HTMLField(serializers.CharField):
    def to_representation(self, value):
        return str(BeautifulSoup(value, 'html.parser'))

    def to_internal_value(self, data):
        return data


class TravelGuideSerializer(serializers.ModelSerializer):
    guide_content = serializers.SerializerMethodField()
    
    class Meta:
        model = TravelGuide
        fields = '__all__'
        depth = 2
        ordering = ['-created_at']
    
    def get_guide_content(self, obj):
        html_string = obj.guide_content
        soup = BeautifulSoup(html_string, 'html.parser')
        toc_div = soup.find('div', class_='mce-toc')
        if toc_div is not None:
            toc_div.extract()
        updated_html_string = str(soup)
        return mark_safe(updated_html_string)

class TravelGuideSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelGuide
        exclude = ['guide_content']
        depth = 1
        ordering = ['-created_at']

class NavBarTravelGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelGuide
        fields = ('id','title','slug','icon')

class LandingTravelGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelGuide
        fields = ('id','title','slug','icon','meta_title')

class TravelGuideSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelGuide
        fields = ('slug',)
        depth = 1