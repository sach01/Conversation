from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def test_page(request):
    return Response({"message": "Welcome to Maramari App API!"})

import csv
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import SentencePair
from django.http import JsonResponse

from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import csv
from .models import SentencePair

from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import csv
from .models import SentencePair
import logging

logger = logging.getLogger(__name__)

def import_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage(location='media/ensw')
        filename = fs.save(csv_file.name, csv_file)
        file_path = fs.path(filename)

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                if 'English_sentence' not in reader.fieldnames or 'Kiswahili_sentence' not in reader.fieldnames:
                    return JsonResponse({"error": "CSV file format incorrect. Must contain 'English_sentence' and 'Kiswahili_sentence' headers."}, status=400)

                for row in reader:
                    SentencePair.objects.create(
                        english_sentence=row['English_sentence'],
                        kiswahili_sentence=row['Kiswahili_sentence']
                    )
            return JsonResponse({"message": "CSV data imported successfully!"})
        except Exception as e:
            logger.error(f"Error processing CSV: {str(e)}")
            return JsonResponse({"error": f"Error processing CSV: {str(e)}"}, status=500)

    return render(request, 'import_csv.html')

def list_data(request):
    sentence_pairs = SentencePair.objects.all()
    return render(request, 'list_data.html', {'sentence_pairs': sentence_pairs})

##################################################################
def dashboard(request):
    user = request.user

    context = {
        'is_admin': user.has_role('admin'),
        'is_data_collector': user.has_role('Data Collector'),
        'is_feedback_contributor': user.has_role('Feedback Contributor'),
        'is_moderator': user.has_role('Moderator'),
    }
    # Logic for the dashboard view
    return render(request, 'dashboard.html')





################################################################
# maramari_app/views.py

from django.shortcuts import render, redirect
from .models import SentencePair, TranslateSentence
from .utils import (
    allocate_sentences_to_user,
    add_points_to_user,
    check_translation_completion,
    unlock_timed_out_translations,
    handle_expired_allocations,
    calculate_progress
)
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from accounts.decorators import group_required  # Importing the decorator from accounts app

@login_required
@group_required('admin')  # Restrict view to data collectors
def translate_view(request):
    user = request.User

    # Unlock any timed-out translations
    unlock_timed_out_translations()

    # Handle expired allocations
    handle_expired_allocations()

    # Check if the user has any allocated sentences that are not translated and not locked
    user_allocations = TranslateSentence.objects.filter(user=user, is_translated=False, locked_by__isnull=True)

    if not user_allocations.exists():
        # Allocate a new batch based on the user's level
        allocate_sentences_to_user(user)
        user_allocations = TranslateSentence.objects.filter(user=user, is_translated=False)

    # Lock a sentence for the user to work on
    if user_allocations.exists():
        allocation = user_allocations.first()
        allocation.locked_by = user
        allocation.time_started = timezone.now()
        allocation.save()

        # Calculate user progress
        progress_percentage, remaining_tasks = calculate_progress(user)

        context = {
            'sentence_pair': allocation.sentence_pair,
            'progress_percentage': progress_percentage,
            'remaining_tasks': remaining_tasks
        }
        return render(request, 'translate.html', context)

    # If no allocations are available, inform the user
    context = {
        'message': "No sentences available for translation at the moment. Please check back later."
    }
    return render(request, 'translate.html', context)

@login_required
def submit_translation(request, sentence_pair_id):
    if request.method == 'POST':
        translation_text = request.POST.get('translation')
        sentence_pair = SentencePair.objects.get(id=sentence_pair_id)

        try:
            # Fetch the allocation
            allocation = TranslateSentence.objects.get(user=request.user, sentence_pair=sentence_pair, is_translated=False)
        except TranslateSentence.DoesNotExist:
            # Handle case where allocation does not exist
            return redirect('translate')

        # Update the translation
        allocation.translation = translation_text
        allocation.is_translated = True
        allocation.locked_by = None
        allocation.time_completed = timezone.now()
        allocation.save()

        # Add points to the user
        add_points_to_user(request.user, 50)  # Example: 50 points per translation

        # Check if the user completed their batch and allocate next if necessary
        check_translation_completion(request.user)

        return redirect('translate')

    return redirect('translate')

# maramari_app/views.py

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Count
from django.shortcuts import render
from .models import UserProfile, TranslateSentence
from django.utils import timezone
	
from django.db.models import F
from django.utils import timezone
from django.db.models import F


@staff_member_required
def analytics_view(request):
    # Average time taken per translation
    avg_time = TranslateSentence.objects.filter(is_translated=True).annotate(
        duration=F('time_completed') - F('time_started')  # Use F() from django.db.models
    ).aggregate(average_duration=Avg('duration'))

    # Number of translations per user
    translations_per_user = UserProfile.objects.annotate(
        translation_count=Count('user__translations')
    ).order_by('-translation_count')[:10]

    # Most difficult sentences (e.g., longest time to translate)
    difficult_sentences = TranslateSentence.objects.filter(is_translated=True).annotate(
        duration=F('time_completed') - F('time_started')  # Use F() from django.db.models
    ).order_by('-duration')[:10]

    context = {
        'avg_time': avg_time['average_duration'],
        'translations_per_user': translations_per_user,
        'difficult_sentences': difficult_sentences
    }
    return render(request, 'analytics.html', context)


## 'difficult_sentences': difficult_sentences




##############################################################

'''
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

@api_view(['GET', 'POST'])
def register_user(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')

        if email is None or password is None:
            return render(request, 'register.html', {'error': 'Email and password are required'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email is already in use'})
        
        # Create the user
        User.objects.create(
            email=email,
            username=username,
            password=make_password(password)
        )
        return redirect('token_obtain_pair')
    
    return render(request, 'register.html')

# Custom JWT Login view (using email and password)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Logout view (blacklisting tokens)
@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data['refresh_token']
        token = RefreshToken(refresh_token)
        token.blacklist()  # Blacklist the refresh token
        return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            return redirect('home')  # Redirect to a homepage or dashboard after login
        else:
            # If authentication fails
            messages.error(request, 'Invalid email or password')

    return render(request, 'login.html')
'''