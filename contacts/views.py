from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
from smtplib import SMTPException
from django.contrib.auth.models import User
import logging

# Set up logging for error handling
logger = logging.getLogger(__name__)

# Create your views here.
def inquiry(request):
    if request.method == 'POST':
        car_id = request.POST['car_id']
        car_title = request.POST['car_title']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        customer_need = request.POST['customer_need']
        city = request.POST['city']
        state = request.POST['state']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        
        user_id = request.user.id if request.user.is_authenticated else None

        # Check if the user has already made an inquiry for this car
        if user_id and Contact.objects.filter(car_id=car_id, user_id=user_id).exists():
            messages.error(request, 'You have already made an inquiry about this car! Please wait for confirmation.')
            return redirect(f'/cars/{car_id}')

        # Save the contact inquiry to the database
        contact = Contact(
            car_id=car_id,
            car_title=car_title,
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            customer_need=customer_need,
            city=city,
            state=state,
            email=email,
            phone=phone,
            message=message
        )
        contact.save()

        # Try to get the admin email and send notification
        admin_info = User.objects.filter(is_superuser=True).first()
        if admin_info:
            admin_email = admin_info.email
            try:
                send_mail(
                    'New Car Inquiry',
                    f'You have a new inquiry for the car {car_title}. Please login to your admin panel for more info.',
                    'ugwuanyitukwasi@gmail.com',  # From email
                    [admin_email],  # To email
                    fail_silently=False,
                )
                logger.info("Inquiry email sent successfully.")
            except SMTPException as e:
                logger.error(f"SMTPException: Failed to send email - {e}")
                messages.error(request, 'Failed to send inquiry notification to admin. Please try again later.')
            except Exception as e:
                logger.error(f"Error sending email: {e}")
                messages.error(request, 'An unexpected error occurred while sending the inquiry email.')
        else:
            logger.error("No superuser found. Cannot send inquiry email.")
            messages.error(request, 'Admin email not found. Please contact support.')

        # Success message for the user
        messages.success(request, 'Your request has been submitted, we will get back to you shortly.')
        return redirect(f'/cars/{car_id}')






""" from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your views here.
def inquiry(request):
    if request.method == 'POST':
        car_id = request.POST['car_id']
        car_title = request.POST['car_title']
        user_id = request.POST['user_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        customer_need = request.POST['customer_need']
        city = request.POST['city']
        state = request.POST['state']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        #User has made inquiry ones
        if request.user.is_authenticated:
            user_id = request.user.id
            has_created = Contact.objects.all().filter(car_id=car_id, user_id=user_id)
            if has_created:
                messages.error(request, 'You have already made an inquiry about this car, Please wait untill we get bact to you!.')
                return redirect('/cars/'+car_id)

        contact = Contact(
            car_id=car_id,
            car_title=car_title,
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            customer_need=customer_need,
            city=city,
            state=state,
            email=email,
            phone=phone,
            message=message
        )

        admin_info = User.objects.get(is_superuser=True)
        admin_email = admin_info.email
        contact.save()
        try:
            send_mail(
                'New Car Inquiry',
                'You have a new inquiry for the car ' + car_title + '. Please login to your admin panel for more info',
                'ugwuanyitukwasi@gmail.com',# from email
                [admin_email],
                fail_silently=False,
            )
        except Exception as e:
            print('Email send error:', e)
            messages.warning(request, 'Inquiry saved but failed to send email notification')    


        messages.success(request, 'Your request has been submitted, we will get back to you shortly!.')
        return redirect('/cars/'+car_id) """