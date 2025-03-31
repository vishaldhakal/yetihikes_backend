from django.shortcuts import render, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FAQ, FAQCategory, LegalDocument, FeaturedTour, TeamMember, Testimonial, SiteConfiguration, Affiliations, Partners, DestinationNavDropdown, OtherActivitiesNavDropdown, InnerDropdown, ClimbingNavDropdown, TreekingNavDropdown, NewsletterSubscription
from .serializers import FAQSerializer, LegalDocumentSerializer, FeaturedTourSerializer, FAQCategorySerializer, TeamMemberSlugSerializer, TestimonialSerializer, TeamMemberSerializer, AffiliationsSerializer, PartnersSerializer, SiteConfigurationSerializer, DestinationNavDropdownSerializer, OtherActivitiesNavDropdownSerializer, ClimbingNavDropdownSerializer, TreekingNavDropdownSerializer, LandingTeamMemberSerializer, LandingFeaturedTourSerializer
from blog.models import Post
from blog.serializers import PostSmallSerializer, LandingPagePostSerializer
from activity.models import ActivityCategory, Activity, ActivityEnquiry, ActivityBooking, DepartureDate, ActivityRegion
from activity.serializers import ActivityCategorySerializer, ActivitySmallSerializer, ActivityCategory2Serializer, NavBarActivityRegionSerializer
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from activity.serializers import ActivityBooking2Serializer, DepartureDateSerializer, navBarActivitySmallSerializer
from datetime import date
from guide.models import TravelGuide
from guide.serializers import TravelGuideSmallSerializer, NavBarTravelGuideSerializer, LandingTravelGuideSerializer
from activity.models import Cupon
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv
import os

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")


def send_brevo_contact_email(name, email, phone, message):
    """Helper function to send email via Brevo API"""
    try:
        # Configure API client
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = BREVO_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration))

        # Render email template
        context = {
            "name": name,
            "email": email,
            "phone": phone or "Not provided",
            "message": message
        }
        html_content = render_to_string("contact_email.html", context)

        # Prepare email request
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": "info@yetihikes.com"},
                {"email": email}],
            sender={"email": "info@yetihikes.com", "name": "Yeti Hikes"},
            subject=f"Contact Form Submission from {name}",
            html_content=html_content,
            reply_to={"email": "info@yetihikes.com", "name": "Yeti Hikes"}
        )

        # Send email
        api_instance.send_transac_email(send_smtp_email)
        return True, None

    except ApiException as e:
        return False, f"Brevo API error: {str(e)}"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"


@api_view(["POST"])
def ContactFormSubmission(request):
    if request.method == "POST":
        try:
            # Get data from either POST or request.data (for JSON)
            data = request.POST or request.data

            # Get required fields
            name = data.get("name", "").strip()
            email = data.get("email", "").strip()
            phone = data.get("phone", "").strip()
            message = data.get("message", "").strip()

            # Basic validation
            if not all([name, email, message]):
                return Response({
                    "error": "Missing required fields",
                    "message": "Please provide name, email and message"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Send email using Brevo
            success, error = send_brevo_contact_email(
                name, email, phone, message)

            if not success:
                return Response({
                    "error": "Failed to send email",
                    "details": error
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                "message": "Contact form submitted successfully",
                "data": {
                    "name": name,
                    "email": email,
                    "phone": phone or "Not provided"
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": "An error occurred while processing your request",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        "error": "Method not allowed"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def send_brevo_inquiry_email(name, email, phone, message, activity, slug):
    """Helper function to send inquiry email via Brevo API"""
    try:
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = BREVO_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration))

        context = {
            "name": name,
            "email": email,
            "phone": phone or "Not provided",
            "message": message,
            "activity": activity,
            "slug": slug
        }
        html_content = render_to_string("inquiry_email.html", context)

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": "info@yetihikes.com"},
                {"email": email}],
            sender={"email": "info@yetihikes.com", "name": "Yeti Hikes"},
            subject=f"Activity Inquiry from {name} - {activity}",
            html_content=html_content,
            reply_to={"email": "info@yetihikes.com", "name": "Yeti Hikes"}
        )

        api_instance.send_transac_email(send_smtp_email)
        return True, None

    except ApiException as e:
        return False, f"Brevo API error: {str(e)}"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"


@api_view(["POST"])
def InquirySubmission(request):
    if request.method == "POST":
        try:
            data = request.POST or request.data
            name = data.get("name", "").strip()
            email = data.get("email", "").strip()
            phone = data.get("phone", "").strip()
            message = data.get("message", "").strip()
            slug = data.get("slug", "").strip()

            if not all([name, email, message, slug]):
                return Response({
                    "error": "Missing required fields",
                    "message": "Please provide name, email, message and activity"
                }, status=status.HTTP_400_BAD_REQUEST)

            actt = Activity.objects.get(slug=slug)

            # Create inquiry record
            neww = ActivityEnquiry.objects.create(
                activity=actt,
                name=name,
                email=email,
                message=message,
                phone=phone or "No Number"
            )
            neww.save()

            # Send email using Brevo
            success, error = send_brevo_inquiry_email(
                name, email, phone, message,
                actt.activity_title, slug
            )

            if not success:
                return Response({
                    "error": "Failed to send email",
                    "details": error
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                "message": "Inquiry submitted successfully"
            }, status=status.HTTP_200_OK)

        except Activity.DoesNotExist:
            return Response({
                "error": "Activity not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "error": "An error occurred",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        "error": "Method not allowed"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def send_brevo_plan_trip_email(context):
    """Helper function to send trip plan email via Brevo API"""
    try:
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = BREVO_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration))

        html_content = render_to_string("plan_trip_email.html", context)

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": "info@yetihikes.com"},
                {"email": context["email"]}],
            sender={"email": "info@yetihikes.com", "name": "Yeti Hikes"},
            subject=f"Trip Plan Request from {context['name']} - {context['activity_title']}",
            html_content=html_content,
            reply_to={"email": "info@yetihikes.com", "name": "Yeti Hikes"}
        )

        api_instance.send_transac_email(send_smtp_email)
        return True, None

    except ApiException as e:
        return False, f"Brevo API error: {str(e)}"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"


@api_view(["POST"])
def PlanTripSubmit(request):
    if request.method == "POST":
        try:
            data = request.POST or request.data
            required_fields = ["name", "email", "slug", "no_of_people",
                               "no_of_days", "arrival", "departure",
                               "budget_from", "budget_to"]

            if not all(data.get(field, "").strip() for field in required_fields):
                return Response({
                    "error": "Missing required fields"
                }, status=status.HTTP_400_BAD_REQUEST)

            actt = Activity.objects.get(slug=data["slug"])

            context = {
                "name": data["name"],
                "email": data["email"],
                "phone": data.get("phone", ""),
                "message": data.get("message", ""),
                "no_of_people": data["no_of_people"],
                "no_of_days": data["no_of_days"],
                "arrival": data["arrival"],
                "departure": data["departure"],
                "budget_from": data["budget_from"],
                "budget_to": data["budget_to"],
                "activity_title": actt.activity_title,
                "slug": data["slug"]
            }

            success, error = send_brevo_plan_trip_email(context)

            if not success:
                return Response({
                    "error": "Failed to send email",
                    "details": error
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                "message": "Trip plan request submitted successfully"
            }, status=status.HTTP_200_OK)

        except Activity.DoesNotExist:
            return Response({
                "error": "Activity not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "error": "An error occurred",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        "error": "Method not allowed"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def send_brevo_booking_email(context):
    """Helper function to send booking email via Brevo API"""
    try:
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = BREVO_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration))

        html_content = render_to_string("booking_email.html", context)

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": "info@yetihikes.com"},
                {"email": context["email"]}],
            sender={"email": "info@yetihikes.com", "name": "Yeti Hikes"},
            subject=f"Booking Confirmation from {context['name']} - {context['activity']}",
            html_content=html_content,
            reply_to={"email": "info@yetihikes.com", "name": "Yeti Hikes"}
        )

        api_instance.send_transac_email(send_smtp_email)
        return True, None

    except ApiException as e:
        return False, f"Brevo API error: {str(e)}"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"


@api_view(["POST"])
def BookingSubmission(request):
    if request.method == "POST":
        try:
            data = request.POST or request.data

            # Required fields validation
            required_fields = ["name", "address", "email",
                               "no_of_guests", "total_price", "booking_date", "slug"]
            if not all(data.get(field, "") for field in required_fields):
                return Response({
                    "error": "Missing required fields",
                    "message": "Please provide all required booking information"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Get required fields
            name = data.get("name")
            address = data.get("address")
            email = data.get("email")
            no_of_guests = int(data.get("no_of_guests", 0))
            total_price = float(data.get("total_price", 0.0))
            booking_date_str = data.get("booking_date")
            cupon_code = data.get("cupon_code", "")

            # Get activity
            act = Activity.objects.get(slug=data["slug"])

            # Handle coupon if provided
            cupon = None
            if cupon_code:
                try:
                    cupon = Cupon.objects.get(code=cupon_code)
                    total_price = total_price * (1 - cupon.discount / 100)
                except Cupon.DoesNotExist:
                    pass

            # Optional fields
            phone = data.get("phone", "")
            message = data.get("message", "")
            arrival_date_str = data.get("arrival_date", "")
            departure_date_str = data.get("departure_date", "")
            private_booking = data.get("private_booking", "False")

            # Create booking context for email
            context = {
                "name": name,
                "email": email,
                "phone": phone,
                "message": message,
                "total_price": total_price,
                "no_of_guests": no_of_guests,
                "booking_date": booking_date_str,
                "activity": act.activity_title,
                "slug": data["slug"],
            }

            # Add emergency contact details to context
            emergency_fields = {
                "emergency_contact_name": data.get("emergency_contact_name", ""),
                "emergency_address": data.get("emergency_address", ""),
                "emergency_phone": data.get("emergency_phone", ""),
                "emergency_email": data.get("emergency_email", "")
            }
            context.update({k: v for k, v in emergency_fields.items() if v})

            # Send email using Brevo
            success, error = send_brevo_booking_email(context)

            if not success:
                return Response({
                    "error": "Failed to send email confirmation",
                    "details": error
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Create booking record
            booking_data = {
                "activity": act,
                "name": name,
                "address": address,
                "email": email,
                "no_of_guests": no_of_guests,
                "total_price": total_price,
                "booking_date": booking_date_str,
            }

            if cupon:
                booking_data["cupon_code"] = cupon

            new_booking = ActivityBooking.objects.create(**booking_data)

            # Update optional fields
            optional_fields = {
                'is_private': private_booking == "True" if private_booking else None,
                'phone': phone or None,
                'message': message or None,
                'arrival_date': arrival_date_str or None,
                'departure_date': departure_date_str or None,
                'emergency_contact_name': emergency_fields['emergency_contact_name'] or None,
                'emergency_address': emergency_fields['emergency_address'] or None,
                'emergency_phone': emergency_fields['emergency_phone'] or None,
                'emergency_email': emergency_fields['emergency_email'] or None,
                'emergency_relationship': data.get('emergency_relationship') or None
            }

            # Update booking with non-None optional fields
            for field, value in optional_fields.items():
                if value is not None:
                    setattr(new_booking, field, value)

            new_booking.save()

            # Update departure date booked seats if applicable
            try:
                departure_date = DepartureDate.objects.get(
                    activity=act, date=booking_date_str)
                departure_date.booked_seats += no_of_guests
                departure_date.save()
            except DepartureDate.DoesNotExist:
                pass

            return Response({
                "message": "Booking submitted successfully",
                "booking_id": new_booking.id
            }, status=status.HTTP_200_OK)

        except Activity.DoesNotExist:
            return Response({
                "error": "Activity not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "error": "An error occurred while processing the booking",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        "error": "Method not allowed"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def Newsletter(request):
    emaill = request.POST.get("email")
    nsss = NewsletterSubscription.objects.create(email=emaill)
    nsss.save()
    """ subject = "Newsletter Subscribed" """

    """ body = f"Newsletter Subscribed by {emaill}\n" """

    """ send_mail(subject, body, "info@yetihikes.com",  [emaill,"info@yetihikes.com"], fail_silently=False) """
    return Response({'success': "Subscribed Sucessfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def legaldocuments(request):
    legal_documents = LegalDocument.objects.all()
    legal_documents_serializer = LegalDocumentSerializer(
        legal_documents, many=True)
    return Response({'legal_documents': legal_documents_serializer.data})


@api_view(['GET'])
def faq_list(request):
    faqs = FAQ.objects.all()
    serializer = FAQSerializer(faqs, many=True)

    faq_cats = FAQCategory.objects.all()
    serializer_cat = FAQCategorySerializer(faq_cats, many=True)

    return Response({'faqs': serializer.data, "faq_categories": serializer_cat.data})


@api_view(['GET'])
def navbar(request):
    if request.method == 'GET':
        destination_nav = DestinationNavDropdown.objects.get()
        destination_nav_serializer = DestinationNavDropdownSerializer(
            destination_nav)

        other_nav = OtherActivitiesNavDropdown.objects.get()
        other_nav_serializer = OtherActivitiesNavDropdownSerializer(other_nav)

        acy = ActivityCategory.objects.get(title="Peak Climbing")
        climb_nav = Activity.objects.filter(activity_category=acy)
        climb_nav_serializer = navBarActivitySmallSerializer(
            climb_nav, many=True)

        trek_nav = TreekingNavDropdown.objects.get()
        trek_nav_serializer = TreekingNavDropdownSerializer(trek_nav)

        posts = TravelGuide.objects.all()
        serializer = NavBarTravelGuideSerializer(posts, many=True)

        return Response({
            "destination_nav": destination_nav_serializer.data,
            "other_activities_nav": other_nav_serializer.data,
            "climbing_nav": climb_nav_serializer.data,
            'guides': serializer.data,
            "trekking_nav": trek_nav_serializer.data,
        })


@api_view(['GET'])
def landing_page(request):
    if request.method == 'GET':
        today = date.today()

        teammembers = TeamMember.objects.all()
        teammembers_serializer = LandingTeamMemberSerializer(
            teammembers, many=True)

        testimonial = Testimonial.objects.all()
        testimonial_serializer = TestimonialSerializer(testimonial, many=True)

        posts = Post.objects.all()[:5]
        posts_serializer = LandingPagePostSerializer(posts, many=True)

        activities = FeaturedTour.objects.get()
        serializer_activities = LandingFeaturedTourSerializer(activities)

        activity_category = ActivityCategory.objects.all()[:4]
        serializer_activity_category = ActivityCategory2Serializer(
            activity_category, many=True)

        activity_region = ActivityRegion.objects.all()
        serializer_activity_region = NavBarActivityRegionSerializer(
            activity_region, many=True)

        travel_guide = TravelGuide.objects.all()
        serializer_travel_guide = LandingTravelGuideSerializer(
            travel_guide, many=True)

        departure_dates = DepartureDate.objects.all()
        serializer_departure_dates = DepartureDateSerializer(
            departure_dates, many=True)

        return Response({
            "recent_posts": posts_serializer.data,
            "featured_activities": serializer_activities.data["featured_tours"],
            "popular_activities": serializer_activities.data["popular_tours"],
            "best_selling_activities": serializer_activities.data["best_selling_tours"],
            "banner_activity": serializer_activities.data["banner_tour"],
            "activity_categories": serializer_activity_category.data,
            "activity_regions": serializer_activity_region.data,
            "travel_guides": serializer_travel_guide.data,
            "team_members": teammembers_serializer.data,
            "testimonials": testimonial_serializer.data,
            "departure_dates": serializer_departure_dates.data,
        })


@api_view(['GET'])
def landing_page_hero(request):
    if request.method == 'GET':
        hero_content = SiteConfiguration.objects.get()
        hero_content_serializer = SiteConfigurationSerializer(hero_content)

        return Response({
            "hero_content": hero_content_serializer.data,
        })


@api_view(['GET'])
def all_bookings(request):
    if request.method == 'GET':
        bookings = ActivityBooking.objects.all().order_by('-booking_date')
        bookings_serializer = ActivityBooking2Serializer(bookings, many=True)

        return Response({
            "bookings": bookings_serializer.data,
        })


@api_view(['GET'])
def testimonials(request):
    if request.method == 'GET':
        testimonial = Testimonial.objects.all()
        testimonial_serializer = TestimonialSerializer(testimonial, many=True)

        return Response({
            "testimonials": testimonial_serializer.data,
        })


@api_view(['GET'])
def teams_id(request):
    if request.method == 'GET':
        teammembers = TeamMember.objects.all()
        teammembers_serializer = TeamMemberSlugSerializer(
            teammembers, many=True)

        return Response({
            "team_members": teammembers_serializer.data,
        })


@api_view(['GET'])
def teams(request):
    if request.method == 'GET':
        teammembers = TeamMember.objects.all()
        teammembers_serializer = LandingTeamMemberSerializer(
            teammembers, many=True)

        return Response({
            "team_members": teammembers_serializer.data,
        })


@api_view(['GET'])
def teams_single(request, id):
    if request.method == 'GET':
        teammembers = TeamMember.objects.get(id=id)
        teammembers_serializer = TeamMemberSerializer(teammembers)

        return Response({
            "team_member": teammembers_serializer.data,
        })
