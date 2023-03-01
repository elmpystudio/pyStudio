from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import random
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

otp_dict = {}


@permission_classes([AllowAny])
@csrf_exempt
@api_view(['POST'])
def register(request):
    email = request.POST.get("email")
    if email:
        otp = random.randint(1000, 9999)
        otp_dict[email] = otp
        # Send the OTP to the user's email here
        subject = 'Account Verification OTP'
        message = 'Your OTP for account verification is: {}'.format(otp)
        from_email = 'your_email@example.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return JsonResponse({"message": "OTP sent to email"})


@csrf_exempt
@api_view(['POST'])
def verify(request):
    email = request.POST.get("email")
    otp = request.POST.get("otp")
    if email and otp:
        if email in otp_dict and otp_dict[email] == int(otp):
            del otp_dict[email]  # Delete the OTP for the user after successful verification
            return JsonResponse({"message": "Verification successful"})
        else:
            return JsonResponse({"message": "Invalid OTP"})
    else:
        return JsonResponse({"message": "Email or OTP not provided"})
