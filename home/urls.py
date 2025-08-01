from django.urls import path, include
from . import views

urlpatterns = [
    path('landing-page/', views.landing_page),
    path('landing-recent-posts/', views.landing_recent_posts),
    path('landing-activity-categories/', views.landing_activity_categories),
    path('landing-activity-regions/', views.landing_activity_regions),
    path('landing-travel-guides/', views.landing_travel_guides),
    path('landing-team-members/', views.landing_team_members),
    path('landing-testimonials/', views.landing_testimonials),
    path('landing-departure-dates/', views.landing_departure_dates),
    path('site-config/', views.landing_page_hero),
    path('all-bookings/', views.all_bookings),
    path('testimonials/', views.testimonials),
    path('legaldocuments/', views.legaldocuments),
    path('team-members/', views.teams),
    path('team-members-id/', views.teams_id),
    path('navbar/', views.navbar),
    path('faqs/', views.faq_list),
    path('contact-form-submit/', views.ContactFormSubmission),
    path('enquiry-submit/', views.InquirySubmission),
    path('plan-trip-submit/', views.PlanTripSubmit),
    path('booking-submit/', views.BookingSubmission),
    path('newsletter-submit/', views.Newsletter),
    path('team-single/<int:id>/', views.teams_single),

    # New separated tour endpoints
    path('landing-featured-activities/', views.get_featured_tours),
    path('landing-popular-activities/', views.get_popular_tours),
    path('landing-bestselling-activities/', views.get_best_selling_tours),
    path('landing-banner-activities/', views.get_banner_tour),
]
