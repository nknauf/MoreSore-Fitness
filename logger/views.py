from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import login


from datetime import date
import requests
import os

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import MuscleGroup, Equipment, Exercise, DailyLog, Workout, WorkoutExercise, UserProfile, ExerciseProgress, StageWorkout, Picture, MealEntry
from .serializers import WorkoutSerializer, AIWorkoutCreateSerializer, AIMealCreateSerializer, MealEntrySerializer
from .utils import update_exercise_progress
from .forms import RegisterForm


WORKOUT_AGENT_URL = 'http://143.198.113.171:5678/webhook/workout-agent'
MEAL_AGENT_URL = 'http://143.198.113.171:5678/webhook/meal-agent'


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # automatically log in new user
            messages.success(request, "Account created successfully!")
            return redirect('home')  # redirect to dashboard
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def home(request):
    daily_log, _ = DailyLog.objects.get_or_create(
        user=request.user,
        date=timezone.localdate()
    )
    workouts = daily_log.workouts.all().order_by('-date', '-created_at')
    meals = daily_log.meals.all().order_by('-date', '-created_at')
    pictures = Picture.objects.filter(user=request.user).order_by('-uploaded_at')[:9]

    staged = StageWorkout.objects.filter(user=request.user).first()
    staged_data = staged.data if staged else None
    
    return render(request, "logger/home.html", {
        "daily_log": daily_log,
        "workouts": workouts,
        "meals": meals,
        "staged_workout": staged_data,
        "pictures": pictures
    })

@login_required
@require_POST
def upload_picture(request):
    """Handles uploading a pump pic from mobile or desktop."""
    image_file = request.FILES.get('image')
    if not image_file:
        return JsonResponse({'error': 'No image provided'}, status=400)

    Picture.objects.create(user=request.user, image=image_file)
    return redirect('home')

@login_required
@require_POST
def delete_picture(request, pic_id):
    pic = get_object_or_404(Picture, id=pic_id, user=request.user)
    pic.delete()
    return redirect('home')

@api_view(['POST'])
def trigger_agent(request):
    try:
        user_input = request.data.get('input', '')
        user_id = request.data.get('user_id', 1)

        if not user_input:
            return Response({"error": "Input is required"}, status=400)
        
        input_date = request.data.get('date')
        if not input_date:
            input_date = timezone.localdate().isoformat()
        
        workout_keywords = ["workout", "sets", "reps", "bench", "curl", "press", "squat"]
        meal_keywords = ["meal", "calorie", "calories", "cals", "protein", "breakfast", "lunch", "dinner", "food", "snack"]

        input_lower = user_input.lower()
        if any(word in input_lower for word in meal_keywords):
            target_url = MEAL_AGENT_URL
            agent_type = "meal"
        else:
            target_url = WORKOUT_AGENT_URL
            agent_type = "workout"
        
        # callback_url = "https://manlike-dextrously-aracely.ngrok-free.dev/api/create-workout-from-agent/"
        
        payload = {
            'input': user_input,
            'user_id': user_id,
            'date': input_date,
            'callback_url': f"https://manlike-dextrously-aracely.ngrok-free.dev/api/create-{agent_type}-from-agent/"
        }
        
        # Test 3: Try the network request with detailed error info
        try:
            response = requests.post(target_url, json=payload, timeout=10)  # Shorter timeout for testing
            
            return Response({
                'message': f"{agent_type.capitalize()} agent triggered successfully!",
                'n8n_status': response.status_code,
                'n8n_response': response.text[:500],  # First 500 chars only
                'payload_sent': payload
            })
            
        except requests.exceptions.ConnectTimeout:
            return Response({'error': 'Connection timeout to n8n'}, status=500)
        except requests.exceptions.ConnectionError as e:
            return Response({'error': f'Connection error to n8n: {str(e)}'}, status=500)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Request error: {str(e)}'}, status=500)
            
    except Exception as e:
        return Response({'error': f'Unexpected error: {str(e)}'}, status=500)
    

@csrf_exempt
@api_view(['POST'])
def create_workout_from_agent(request):
    """
    This endpoint receives the processed workout data back from n8n and creates the actual workout in the database
    """
    try:
        workout_data = request.data
        serializer = AIWorkoutCreateSerializer(data=workout_data)
        if serializer.is_valid():
            workout = serializer.save()
            
            # workout_date = timezone.localdate()
            # invalid_dates = {None, date(1900,1,1), date(2024,1,1)}
            # if workout.date not in invalid_dates:
            #     workout_date = workout.date

            daily_log, created = DailyLog.objects.get_or_create(
                user=workout.user, 
                date=workout.date,
            )
            daily_log.workouts.add(workout)
            workout_serialized = WorkoutSerializer(workout)
            update_exercise_progress(workout.user, workout)
            return Response({'message': 'Workout created successfully', 'workout': workout_serialized.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Failed to create workout', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@login_required
@csrf_exempt
def finalize_staged_workout(request):
    staged = StageWorkout.objects.filter(user=request.user).first()
    if not staged:
        return redirect('home')
    data = staged.data
    serializer = AIWorkoutCreateSerializer(data=data)
    if serializer.is_valid():
        workout = serializer.save()
        daily_log, _ = DailyLog.objects.get_or_create(user=request.user, date=timezone.localdate())
        daily_log.workouts.add(workout)
        staged.delete()
        return redirect('home')
    else:
        return JsonResponse({'error': serializer.errors}, status=400)
    
@login_required
def discard_staged_workout(request):
    StageWorkout.objects.filter(user=request.user).delete()
    return redirect('home')
    
@csrf_exempt
@api_view(['POST'])
def create_meal_from_agent(request):
    """
    Receives structured meal data from n8n and creates a MealEntry + links to DailyLog.
    """
    try:
        meal_data = request.data
        serializer = AIMealCreateSerializer(data=meal_data)
        if serializer.is_valid():
            meal = serializer.save()

            # meal_date = timezone.localdate()
            # invalid_dates = {None, date(1900,1,1), date(2024,1,1)}
            # if meal.date not in invalid_dates:
            #     meal_date = meal.date

            daily_log, _ = DailyLog.objects.get_or_create(
                user=meal.user, 
                date=meal.date
            )
            daily_log.meals.add(meal)
            daily_log.save()
            meal_serialized = MealEntrySerializer(meal)
            return Response({'message': 'Meal created successfully'}, status=201)
        else:
            return Response({'error': 'Invalid data', 'details': serializer.errors}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_recent_workouts(request):
    """
    Helper endpoint to get recent workouts (for your chatbot to show)
    """
    user_id = request.GET.get('user_id', 1)
    try:
        user = User.objects.get(id=user_id)
        workouts = user.workout_set.all()[:5]  # Last 5 workouts
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, 
                      status=status.HTTP_404_NOT_FOUND)
    

@login_required
def delete_workout(request, workout_id):
    """
    Delete workout function and removes it from the user's daily_log
    """
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    daily_log = DailyLog.objects.filter(
        user=request.user,
        date=workout.date
    ).first()
    
    if daily_log:
        daily_log.workouts.remove(workout)

    workout.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def delete_meal(request, meal_id):
    """
    Delete meal function and removes it from daily log
    """
    meal = get_object_or_404(MealEntry, id=meal_id, user=request.user)
    daily_log = DailyLog.objects.filter(
        user=request.user,
        date=meal.date
    ).first()

    if daily_log:
        daily_log.meals.remove(meal)
    meal.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

    
# @login_required
# def view_logs_by_date(request):
#     """Display meals and workouts for a given date."""
#     selected_date = request.GET.get("date", timezone.localdate().isoformat())

#     # Fetch or create daily log
#     daily_log = DailyLog.objects.filter(user=request.user, date=selected_date).first()

#     meals = daily_log.meals.all() if daily_log else []
#     workouts = daily_log.workouts.all() if daily_log else []

#     total_calories = sum(m.calories for m in meals)
#     total_protein = sum(m.protein for m in meals)
#     total_carbs = sum(m.carbs for m in meals)
#     total_fats = sum(m.fats for m in meals)

#     context = {
#         "selected_date": selected_date,
#         "meals": meals,
#         "workouts": workouts,
#         "total_calories": total_calories,
#         "total_protein": total_protein,
#         "total_carbs": total_carbs,
#         "total_fats": total_fats,
#     }
#     return render(request, "logger/view_logs_by_date.html", context)

@login_required
def progress(request):
    """
    Combined dashboard: shows daily meals/workouts by date
    and detailed exercise progress trends below.
    """
    from collections import defaultdict
    from datetime import date

    # --- 1. Handle date picker for daily logs ---
    selected_date = request.GET.get("date", timezone.localdate().isoformat())
    daily_log = DailyLog.objects.filter(user=request.user, date=selected_date).first()

    meals = daily_log.meals.all() if daily_log else []
    workouts = daily_log.workouts.all() if daily_log else []

    total_calories = sum(m.calories for m in meals)
    total_protein = sum(m.protein for m in meals)
    total_carbs = sum(m.carbs for m in meals)
    total_fats = sum(m.fats for m in meals)

    # --- 2. Handle exercise progress filtering ---
    selected_exercise_id = request.GET.get("exercise")
    progresses = ExerciseProgress.objects.filter(user=request.user).select_related("exercise")

    grouped_progress = defaultdict(list)
    if selected_exercise_id:
        progresses = progresses.filter(exercise__id=selected_exercise_id)
        exercise_name = progresses.first().exercise.name if progresses.exists() else None
        grouped_progress[exercise_name] = list(progresses.order_by("date"))
    else:
        # Default: show recent 5 exercises (optional)
        recent = progresses.order_by("-date")[:50]
        for p in recent:
            grouped_progress[p.exercise.name].append(p)

    # --- 3. Get exercise list for dropdown ---
    all_exercises = (
        ExerciseProgress.objects.filter(user=request.user)
        .select_related("exercise")
        .order_by("exercise__name")
        .values_list("exercise__id", "exercise__name")
        .distinct()
    )

    context = {
        # Daily log data
        "selected_date": selected_date,
        "meals": meals,
        "workouts": workouts,
        "total_calories": total_calories,
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_fats": total_fats,

        # Progress data
        "grouped_progress": grouped_progress,
        "all_exercises": all_exercises,
        "selected_exercise_id": selected_exercise_id,
    }

    return render(request, "logger/progress.html", context)