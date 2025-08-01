from django.urls import path, include
from . import views

urlpatterns = [
    path('activity-detail/<str:slug>/', views.activities_single),
    path('activity-seo/<str:slug>/', views.activity_seo_data),
    path('activity-jsonld/<str:slug>/', views.activity_jsonld_data),
    path('activity-header/<str:slug>/', views.activity_header_data),
    path('activity-related/<str:slug>/', views.related_activities_data),
    path('activity-blogs/<str:slug>/', views.related_blogs_data),
    path('activity-reserve/<str:slug>/', views.activity_reserve_data),
    path('activities/', views.activities_collection),
    path('activities-slug/', views.activities_slug),
    path('activities-search/', views.activities_search),
    path('activity-categories-slug/', views.activities_cat_slug),
    path('activities-regions/', views.activities_regions),
    path('activities-regions/<str:slug>/', views.activities_region_slug),
    path('activities-region-slug/', views.activities_reg_slug),
    path('destinations-slug/', views.destination_slug),
    path('activity-categories/', views.activity_categories_collection),
    path('activity-categories/<str:slug>/', views.activity_category_slug),
    path('cupons/', views.cupons_collection),
    path('activities-all/<str:slug>/', views.activities_all),
    path('activities-region-wise/<str:slug>/', views.activities_all_region),
    path('activities-featured/', views.activities_featured),
    path('sign/', views.sign_view, name='sign_view'),
    path('departure-dates/', views.departure_dates_collection),
]
