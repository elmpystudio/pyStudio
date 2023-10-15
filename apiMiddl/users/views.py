from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
import random
import json
from .models import User
from django.utils import timezone
from .serializers import CustomTokenObtainPairSerializer

class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Please provide username and password.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid username or passwords')

        user_dict = user.to_dict()
        if not user_dict['verified']:
            raise AuthenticationFailed('User account not verified')
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['access']
        user.last_login = timezone.now()
        user.save()
        return Response({'token': str(token), 'user_id': user.id})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        about = request.POST.get('about')
        image = request.POST.get('image')

        if not (username and email and password):
            return JsonResponse({'error': 'Please provide [username, email, password] required fields.'}, status=400)
        
        try:
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                about=about,
                image=image
            )

            send_otp(user)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse({'message': 'User account created successfully.'}, status=201)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def verify(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        otp = data['otp']

        if not (email and otp):
            return JsonResponse({'error': 'Please provide [email, otp] required fields.'}, status=400)

        try:
            user = User.objects.filter(email=email).first()
            if user:
                user_dict = user.to_dict()
                if user_dict['otp_code'] == otp:
                    setattr(user, 'otp_code', None)
                    setattr(user, 'verified', True)
                    user.save()
                    return JsonResponse({'message': "User account verified successfully"}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse({'error': "Invalid data"}, status=401)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


from_email = 'hi@pystudio.org'
subject = 'Account Verification OTP'


def send_otp(user):
    otp = random.randint(1000, 9999)
    message = 'Your OTP for account verification is: {}'.format(otp)

    user_dict = user.to_dict()
    setattr(user, 'otp_code', otp)
    user.save()

    try:
        send_mail(subject, message, from_email, [user_dict['email']], fail_silently=False)
    except Exception as e:
        print(e)

    return True
