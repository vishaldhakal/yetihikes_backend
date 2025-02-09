from .models import Activity,ActivityTestimonialImage,ActivityPricing,ActivityBooking,ActivityEnquiry,ActivityCategory,ItineraryActivity,ActivityImage,Destination,ActivityRegion,ActivityFAQ,ActivityTestimonial,Cupon,DepartureDate
from rest_framework import serializers
from blog.serializers import PostSmallSerializer

class ActivityEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityEnquiry
        fields = ('id',)
        depth = 1

class ActivityTestimonialImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityTestimonialImage
        fields = ('image',)
        depth = 1

class ActivityTestimonialSerializer(serializers.ModelSerializer):
    images = ActivityTestimonialImageSerializer(many=True)
    class Meta:
        model = ActivityTestimonial
        exclude = ('activity',)
        depth = 1

class ActivitySmallestSer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('activity_title','priceSale','slug',)
        depth = 1
        
class ActivityBooking2Serializer(serializers.ModelSerializer):
    activity = ActivitySmallestSer(read_only=True)
    class Meta:
        model = ActivityBooking
        fields = ('id','no_of_guests','booking_date','activity')
        depth = 1
class ActivityBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityBooking
        fields = ('id','no_of_guests','booking_date',)
        depth = 1
class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'
        depth = 2
class NavBarDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Destination
        fields = ('id','name','thumnail_image','thumnail_image_alt_description')

class ActivityRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRegion
        fields = '__all__'
        depth = 1
class NavBarActivityRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRegion
        fields = ('id','title','image','image_alt_description','slug')

class ActivityRegionSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRegion
        fields = ['id','title','slug','image']
        depth = 1

class ActivityRegionSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRegion
        fields = ('id','slug')
        depth = 1

class DestinationSerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ('name',)

class ActivityCategory2Serializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = ('title','image','image_alt_description','subtitle','slug')
        depth = 2

class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = '__all__'
        depth = 2

class ActivityDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model=ActivityCategory
        fields=('id','title')

class NavBarActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = ('id','title','image','image_alt_description')

class ActivityCategorySlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = ('id','slug')

class ActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityImage
        fields = '__all__'

class ActivityPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityPricing
        fields = '__all__'

class ActivityFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityFAQ
        fields = '__all__'

class ItineraryActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryActivity
        fields = '__all__'

class ActivitySmallestSerializer(serializers.ModelSerializer):
    destination = DestinationSerializerSmall()
    class Meta:
        model = Activity
        fields = ('id','slug', 'activity_title','destination','duration','price','priceSale','trip_grade','max_group_size','best_time')

class ActivitySmallSerializer(serializers.ModelSerializer):

    destination = DestinationSerializerSmall()
    enquiries = ActivityEnquirySerializer(many=True,read_only=True)
    class Meta:
        model = Activity
        fields = ('id','slug', 'activity_title', 'activity_category','enquiries','location','duration','price','coverImg','ratings','popular','best_selling','destination','activity_region','priceSale','youtube_link')
        depth = 1
class LandingActivitySmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields=('id','slug','activity_title','location','duration','price','heroImg','coverImg','priceSale','ratings')

class LandingBannerActivitySmallSerializer(serializers.ModelSerializer):
        class Meta:
            model = Activity
            fields=('id','slug','activity_title','location','duration','price','heroImg','coverImg','priceSale','ratings','activity_region')
            depth = 1

class navBarActivitySmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id','slug', 'activity_title','coverImg')

class NavBarActivitySmallSerializer(serializers.ModelSerializer):
    class Meta:
        model=Activity
        fields=('id','activity_title','slug')
        
class ActivitySerializer(serializers.ModelSerializer):
    itinerary = ItineraryActivitySerializer(many=True, read_only=True)
    gallery = ActivityImageSerializer(many=True,read_only=True)
    faqs = ActivityFAQSerializer(many=True,read_only=True)
    enquiries = ActivityEnquirySerializer(many=True,read_only=True)
    testimonials = ActivityTestimonialSerializer(many=True,read_only=True)
    prices = ActivityPricingSerializer(many=True,read_only=True)
    related_activities = ActivitySmallSerializer(many=True,read_only=True)
    related_blogs = PostSmallSerializer(many=True,read_only=True)
    departure_dates = serializers.SerializerMethodField()
    
    def get_departure_dates(self,obj):
        departure_dates = DepartureDate.objects.filter(activity=obj)
        return DepartureDateSerializer2(departure_dates,many=True).data
    
    class Meta:
        model = Activity
        fields = '__all__'
        depth = 2



class ActivitySlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id','slug')

class CuponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupon
        exclude = ('activities',)
        depth = 1

class CuponSerializer2(serializers.ModelSerializer):
    activities = ActivitySmallestSer(many=True,read_only=True)
    class Meta:
        model = Cupon
        fields = '__all__'
        depth = 1

class DepartureDateSerializer(serializers.ModelSerializer):
    activity = ActivitySmallestSer(read_only=True)
    class Meta:
        model = DepartureDate
        fields = '__all__'
        depth = 1

class DepartureDateSerializer2(serializers.ModelSerializer):
    class Meta:
        model = DepartureDate
        fields = ('id','date','booked_seats','max_seats')
        depth = 1
