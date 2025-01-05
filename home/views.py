from django.shortcuts import render,HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FAQ,FAQCategory,LegalDocument,FeaturedTour,TeamMember,Testimonial,SiteConfiguration,Affiliations,Partners,DestinationNavDropdown, OtherActivitiesNavDropdown, InnerDropdown, ClimbingNavDropdown, TreekingNavDropdown,NewsletterSubscription
from .serializers import FAQSerializer,LegalDocumentSerializer,FeaturedTourSerializer,FAQCategorySerializer,TeamMemberSlugSerializer,TestimonialSerializer,TeamMemberSerializer,AffiliationsSerializer,PartnersSerializer,SiteConfigurationSerializer,DestinationNavDropdownSerializer, OtherActivitiesNavDropdownSerializer, ClimbingNavDropdownSerializer, TreekingNavDropdownSerializer
from blog.models import Post
from blog.serializers import PostSmallSerializer
from activity.models import ActivityCategory,Activity,ActivityEnquiry,ActivityBooking,DepartureDate
from activity.serializers import ActivityCategorySerializer,ActivitySmallSerializer,ActivityCategory2Serializer
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from activity.serializers import ActivityBooking2Serializer,DepartureDateSerializer
from datetime import date
from guide.models import TravelGuide
from guide.serializers import TravelGuideSmallSerializer
from activity.models import Cupon



@api_view(["POST"])
def ContactFormSubmission(request):
    if request.method == "POST":
        subject = "Contact Form Submission"
        email = "Yeti Hikes <info@yetihikes.com>"
        headers = {'Reply-To': request.POST["email"]}
        contex = {
            "name": request.POST["name"],
            "email": request.POST["email"],
            "phone": request.POST["phone"],
            "message": request.POST["message"]
        }
        html_content = render_to_string("contactForm.html", contex)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, "You have been sent a Contact Form Submission. Unable to Receive !", email, ["yetihikes790@gmail.com"], headers=headers)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponse("Sucess")
    else:
        return HttpResponse("Not post req")

@api_view(["POST"])
def InquirySubmission(request):
    if request.method == "POST":
        subject = "Enquiry About Activity"
        email = "Yeti Hikes <info@yetihikes.com>"
        headers = {'Reply-To': request.POST["email"]}

        actt = Activity.objects.get(slug=request.POST["slug"])
        if request.POST["phone"]:
            chh = request.POST["phone"]
        else:
            chh = "No Number"

        neww = ActivityEnquiry.objects.create(activity=actt,name=request.POST["name"],email=request.POST["email"],message=request.POST["message"],phone=chh)
        neww.save()

        contex = {
            "name": request.POST["name"],
            "email": request.POST["email"],
            "phone": request.POST["phone"],
            "message": request.POST["message"],
            "activity": actt.activity_title,
            "slug": request.POST["slug"]
        }

        html_content = render_to_string("contactForm2.html", contex)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, "You have been sent a Contact Form Submission. Unable to Receive !", email, ["yetihikes790@gmail.com"], headers=headers)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponse("Sucess")
    else:
        return HttpResponse("Not post req")

@api_view(["POST"])
def PlanTripSubmit(request):
    if request.method == "POST":
        subject = "Customized Trip Enquiry"
        email = "Yeti Hikes <info@yetihikes.com>"
        headers = {'Reply-To': request.POST["email"]}

        actt = Activity.objects.get(slug=request.POST["slug"])

        contex = {
            "name": request.POST["name"],
            "email": request.POST["email"],
            "phone": request.POST["phone"],
            "message": request.POST["message"],
            "noofpeople": request.POST["no_of_people"],
            "noofdays": request.POST["no_of_days"],
            "arrival": request.POST["arrival"],
            "departure": request.POST["departure"],
            "budget_from": request.POST["budget_from"],
            "budget_to": request.POST["budget_to"],
            "activity": actt.activity_title,
            "slug": request.POST["slug"]
        }

        html_content = render_to_string("ContactForm4.html", contex)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, "You have been sent a Contact Form Submission. Unable to Receive !", email, ["yetihikes790@gmail.com"], headers=headers)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponse("Sucess")
    else:
        return HttpResponse("Not post req")

@api_view(["POST"])
def BookingSubmission(request):
    if request.method == "POST":
        subject = "Booking of Activity"
        email = "Yeti Hikes <info@yetihikes.com>"
        headers = {'Reply-To': request.POST["email"]}

        # Required fields
        name = request.POST.get("name")
        address = request.POST.get("address")
        emaill = request.POST.get("email")
        no_of_guests = int(request.POST.get("no_of_guests", 0))
        total_price = float(request.POST.get("total_price", 0.0))
        booking_date_str = request.POST.get("booking_date")
        cupon_code = request.POST.get("cupon_code", "")

        cupon = None

        try:
            cupon = Cupon.objects.get(code=cupon_code)
        except:
            cupon = None

        if cupon:
            total_price = total_price * (1 - cupon.discount / 100)

        # Optional fields
        phone = request.POST.get("phone", "")
        message = request.POST.get("message", "")
        arrival_date_str = request.POST.get("arrival_date", "")
        departure_date_str = request.POST.get("departure_date", "")
        private_booking = request.POST.get("private_booking", "False")

        # Parse dates
        booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d')
        arrival_date = datetime.strptime(arrival_date_str, '%Y-%m-%d') if arrival_date_str else None
        departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d') if departure_date_str else None

        act = Activity.objects.get(slug=request.POST["slug"])

        # Create context with required fields
        contex = {
            "name": name,
            "email": emaill,
            "phone": phone,
            "message": message,
            "total_price": total_price,
            "no_of_guests": no_of_guests,
            "booking_date": booking_date_str,
            "activity": act.activity_title,
            "cupon_code": cupon_code,
            "slug": request.POST["slug"],
        }

        # Add emergency contact details to context only if they exist
        emergency_fields = {
            "emergency_contact_name": request.POST.get("emergency_contact_name", ""),
            "emergency_address": request.POST.get("emergency_address", ""),
            "emergency_phone": request.POST.get("emergency_phone", ""),
            "emergency_email": request.POST.get("emergency_email", "")
        }
        
        # Only add non-empty emergency fields to context
        contex.update({k: v for k, v in emergency_fields.items() if v})

        html_content = render_to_string("contactForm3.html", contex)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, "You have been sent a Contact Form Submission. Unable to Receive !", email, ["yetihikes790@gmail.com"], headers=headers)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # Create booking with required fields
        if cupon:
            new_booking = ActivityBooking.objects.create(
                activity=act,
                name=name,
                address=address,
                email=emaill,
                no_of_guests=no_of_guests,
                total_price=total_price,
                booking_date=booking_date,
                cupon_code=cupon
            )
            try:
                departure_date = DepartureDate.objects.get(activity=act,date=booking_date)
                departure_date.booked_seats += no_of_guests
                departure_date.save()
            except:
                pass
        else:
            new_booking = ActivityBooking.objects.create(
                activity=act,
                name=name,
                address=address,
                email=emaill,
                no_of_guests=no_of_guests,
                total_price=total_price,
                booking_date=booking_date,
            )
            try:
                departure_date = DepartureDate.objects.get(activity=act,date=booking_date)
                departure_date.booked_seats += no_of_guests
                departure_date.save()
            except:
                pass

        optional_fields = {
            'is_private': private_booking == "True" if "private_booking" in request.POST else None,
            'phone': phone if phone else None,
            'message': message if message else None,
            'arrival_date': arrival_date if arrival_date else None,
            'departure_date': departure_date if departure_date else None,
            'emergency_contact_name': emergency_fields['emergency_contact_name'] if emergency_fields['emergency_contact_name'] else None,
            'emergency_address': emergency_fields['emergency_address'] if emergency_fields['emergency_address'] else None,
            'emergency_phone': emergency_fields['emergency_phone'] if emergency_fields['emergency_phone'] else None,
            'emergency_email': emergency_fields['emergency_email'] if emergency_fields['emergency_email'] else None,
            'emergency_relationship': request.POST.get('emergency_relationship', '') if 'emergency_relationship' in request.POST else None
        }

        # Update booking with non-None optional fields
        for field, value in optional_fields.items():
            if value is not None:
                setattr(new_booking, field, value)

        new_booking.save()

        return HttpResponse("Success")
    else:
        return HttpResponse("Not post req")

@api_view(['POST'])
def Newsletter(request):
    emaill = request.POST.get("email")
    nsss = NewsletterSubscription.objects.create(email=emaill)
    nsss.save()
    """ subject = "Newsletter Subscribed" """

    """ body = f"Newsletter Subscribed by {emaill}\n" """

    """ send_mail(subject, body, "info@yetihikes.com",  [emaill,"info@yetihikes.com"], fail_silently=False) """
    return Response({'success': "Subscribed Sucessfully"},status=status.HTTP_200_OK)

@api_view(['GET'])
def legaldocuments(request):
    legal_documents = LegalDocument.objects.all()
    legal_documents_serializer = LegalDocumentSerializer(legal_documents, many=True)
    return Response({'legal_documents': legal_documents_serializer.data})

@api_view(['GET'])
def faq_list(request):
    faqs = FAQ.objects.all()
    serializer = FAQSerializer(faqs, many=True)
    
    faq_cats = FAQCategory.objects.all()
    serializer_cat = FAQCategorySerializer(faq_cats, many=True)
    
    return Response({'faqs': serializer.data,"faq_categories":serializer_cat.data})


@api_view(['GET'])
def navbar(request):
    if request.method == 'GET':
        destination_nav = DestinationNavDropdown.objects.get()
        destination_nav_serializer = DestinationNavDropdownSerializer(destination_nav)

        other_nav = OtherActivitiesNavDropdown.objects.get()
        other_nav_serializer = OtherActivitiesNavDropdownSerializer(other_nav)
        
        acy = ActivityCategory.objects.get(title="Peak Climbing")
        climb_nav = Activity.objects.filter(activity_category=acy)
        climb_nav_serializer = ActivitySmallSerializer(climb_nav,many=True)

        trek_nav = TreekingNavDropdown.objects.get()
        trek_nav_serializer = TreekingNavDropdownSerializer(trek_nav)

        posts = TravelGuide.objects.all()
        serializer = TravelGuideSmallSerializer(posts, many=True)
        
        return Response({
          "destination_nav":destination_nav_serializer.data,
          "other_activities_nav":other_nav_serializer.data,
          "climbing_nav":climb_nav_serializer.data,
          'guides':serializer.data,
          "trekking_nav":trek_nav_serializer.data,
        })


@api_view(['GET'])
def landing_page(request):
    if request.method == 'GET':
        today = date.today()

        teammembers = TeamMember.objects.all()
        teammembers_serializer = TeamMemberSerializer(teammembers,many=True)

        testimonial = Testimonial.objects.all()
        testimonial_serializer = TestimonialSerializer(testimonial,many=True)
        
        hero_content = SiteConfiguration.objects.get()
        hero_content_serializer = SiteConfigurationSerializer(hero_content)

        posts = Post.objects.all()[:5]
        posts_serializer = PostSmallSerializer(posts,many=True)

        activities = FeaturedTour.objects.get()
        serializer_activities = FeaturedTourSerializer(activities)

        activity_category = ActivityCategory.objects.all()
        serializer_activity_category = ActivityCategory2Serializer(activity_category, many=True)

        departure_dates = DepartureDate.objects.all()
        serializer_departure_dates = DepartureDateSerializer(departure_dates, many=True)
        
        return Response({
          "hero_content":hero_content_serializer.data,
          "recent_posts":posts_serializer.data,
          "featured_activities":serializer_activities.data["featured_tours"],
          "popular_activities":serializer_activities.data["popular_tours"],
          "best_selling_activities":serializer_activities.data["best_selling_tours"],
          "favourite_activities":serializer_activities.data["favourite_tours"],
          "banner_activity":serializer_activities.data["banner_tour"],
          "activity_categories":serializer_activity_category.data,
          "team_members":teammembers_serializer.data,
          "testimonials":testimonial_serializer.data,
          "departure_dates":serializer_departure_dates.data,
        })

@api_view(['GET'])
def all_bookings(request):
    if request.method == 'GET':
        bookings = ActivityBooking.objects.all().order_by('-booking_date')
        bookings_serializer = ActivityBooking2Serializer(bookings,many=True)
        
        return Response({
          "bookings":bookings_serializer.data,
        })


@api_view(['GET'])
def testimonials(request):
    if request.method == 'GET':
        testimonial = Testimonial.objects.all()
        testimonial_serializer = TestimonialSerializer(testimonial,many=True)
        
        return Response({
          "testimonials":testimonial_serializer.data,
        })

@api_view(['GET'])
def teams_id(request):
    if request.method == 'GET':
        teammembers = TeamMember.objects.all()
        teammembers_serializer = TeamMemberSlugSerializer(teammembers,many=True)
        
        return Response({
          "team_members":teammembers_serializer.data,
        })

@api_view(['GET'])
def teams(request):
    if request.method == 'GET':
        teammembers = TeamMember.objects.all()
        teammembers_serializer = TeamMemberSerializer(teammembers,many=True)
        
        return Response({
          "team_members":teammembers_serializer.data,
        })

@api_view(['GET'])
def teams_single(request,id):
    if request.method == 'GET':
        teammembers = TeamMember.objects.get(id=id)
        teammembers_serializer = TeamMemberSerializer(teammembers)
        
        return Response({
          "team_member":teammembers_serializer.data,
        })