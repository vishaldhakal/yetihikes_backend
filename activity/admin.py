from django.contrib import admin
from django.db import models
from .models import (
    ActivityTestimonial, ActivityTestimonialImage, ActivityCategory, 
    ActivityBooking, ActivityEnquiry, ActivityPricing, Activity, 
    ItineraryActivity, ActivityImage, Destination, ActivityRegion, ActivityFAQ, Cupon
)
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from tinymce.widgets import TinyMCE

class ItineraryActivityInline(StackedInline):
    model = ItineraryActivity
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
    fieldsets = (
        ("Itinerary Details", {
            "fields": (
                ("day", "title"),
                ("trek_distance", "trek_duration", "highest_altitude"),
                "meals",
                "description"
            )
        }),
    )

class ActivityFAQInline(StackedInline):
    model = ActivityFAQ
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
    fieldsets = (
        ("FAQ Details", {
            "fields": (
                "question",
                "answer",
                "active"
            )
        }),
    )

class ActivityImageInline(TabularInline):
    model = ActivityImage
    fields = ('image', 'image_alt_description')

class ActivityTestimonialImageInline(TabularInline):
    model = ActivityTestimonialImage
    fields = ('image',)

class ActivityPricingInline(TabularInline):
    model = ActivityPricing
    fields = ('group_size', 'price')

class ActivityAdmin(ModelAdmin):
    inlines = [
        ItineraryActivityInline,
        ActivityImageInline,
        ActivityFAQInline,
        ActivityPricingInline,
    ]
    

    list_display = (
        "__str__",
        "price",
        "createdAt",
        "featured",
        "best_selling",
        "popular",
    )
    list_filter = ("featured", "best_selling", "popular", "destination")

    fieldsets = (
        ("Basic Information", {
            "fields": (
                ("activity_title", "slug"),
                ("destination", "activity_category", "activity_region"),
                ("price", "priceSale"),
                ("popular", "best_selling", "featured"),
                ("youtube_link"),
                ("related_blogs"),
                ("related_activities"),
            )
        }),
        ("Meta Information", {
            "fields": (
                "meta_title",
                "meta_description"
            )
        }),
        ("Tour Details", {
            "fields": ("heroImg", "coverImg","location", "duration", "trip_grade","max_group_size", "best_time","ratings","availableStart", "availableEnd","trek_map", "altitude_chart")
        }),
        ("Tour Description", {
            "fields": (
                "tour_description",
                "tour_highlights",
                "tour_includes",
                "tour_excludes",
                "additional_info"
            )
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ['tour_description', 'tour_highlights', 'tour_includes', 'tour_excludes', 'additional_info']:
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, **kwargs)

class ActivityTestimonialAdmin(ModelAdmin):
    inlines = [
        ActivityTestimonialImageInline,
    ]

    fieldsets = (
        ("Testimonial Details", {
            "fields": (
                "activity",
                ("name", "title"),
                "review",
                "rating"
            )
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'review':
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, **kwargs)

class DestinationAdmin(ModelAdmin):
    fieldsets = (
        ("Basic Information", {
            "fields": (
                "name",
                "order",
                "thumnail_image",
                "thumnail_image_alt_description"
            )
        }),
        ("Meta Information", {
            "fields": (
                "meta_title",
                "meta_description"
            )
        }),
        ("Destination Details", {
            "fields": (
                "destination_small_detail",
                "destination_detail"
            )
        })
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'destination_detail':
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, **kwargs)

class ActivityCategoryAdmin(ModelAdmin):
    
    fieldsets = (
        ("Basic Information", {
            "fields": (
                "title",
                "subtitle",
                "destination",
                "slug",
                "image",
                "image_alt_description"
            )
        }),
        ("Meta Information", {
            "fields": (
                "meta_title",
                "meta_description"
            )
        }),
        ("Content", {
            "fields": (
                "content",
            )
        })
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, **kwargs)

class ActivityRegionAdmin(ModelAdmin):
    
    fieldsets = (
        ("Basic Information", {
            "fields": (
                "title",
                "activity_category",
                "slug",
                "image",
                "image_alt_description"
            )
        }),
        ("Meta Information", {
            "fields": (
                "meta_title",
                "meta_description"
            )
        }),
        ("Content", {
            "fields": (
                "content",
            )
        })
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, **kwargs)

class ActivityFAQAdmin(ModelAdmin):
    fieldsets = (
        ("FAQ Details", {
            "fields": (
                "activity",
                "question",
                "answer",
                "active"
            )
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ['question', 'answer']:
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, **kwargs)

class ItineraryActivityAdmin(ModelAdmin):
    fieldsets = (
        ("Itinerary Details", {
            "fields": (
                "activity",
                ("day", "title"),
                ("trek_distance", "trek_duration", "highest_altitude"),
                "meals",
                "description"
            )
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'description':
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, **kwargs)

class ActivityBookingAdmin(ModelAdmin):
    list_display = (
        "__str__",
        "name",
        "booking_date",
        "is_private",
        "is_verified",
    )
    list_filter = ("is_private", "is_verified", "booking_date", "activity")

    fieldsets = (
        ("Booking Information", {
            "fields": (
                "activity",
                ("name", "email", "phone"),
                "address",
                ("no_of_guests", "total_price"),
                ("is_private", "is_verified"),
                ("booking_date", "arrival_date", "departure_date"),
                "message"
            )
        }),
        ("Emergency Contact", {
            "fields": (
                "emergency_contact_name",
                "emergency_address",
                "emergency_phone",
                "emergency_email",
                "emergency_relationship"
            )
        })
    )

admin.site.register(Destination, DestinationAdmin)
admin.site.register(ActivityCategory, ActivityCategoryAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(ItineraryActivity, ItineraryActivityAdmin)
admin.site.register(ActivityImage, ModelAdmin)
admin.site.register(ActivityFAQ, ActivityFAQAdmin)
admin.site.register(ActivityPricing, ModelAdmin)
admin.site.register(ActivityRegion, ActivityRegionAdmin)
admin.site.register(ActivityEnquiry, ModelAdmin)
admin.site.register(ActivityTestimonial, ActivityTestimonialAdmin)
admin.site.register(ActivityBooking, ActivityBookingAdmin)
admin.site.register(Cupon, ModelAdmin)