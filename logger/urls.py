from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('api/trigger-agent/', views.trigger_agent, name='trigger_agent'),
    path('api/create-workout-from-agent/', views.create_workout_from_agent, name='create_workout_from_agent'),
    path('api/create-meal-from-agent/', views.create_meal_from_agent, name='create_meal_from_agent'),
    path('api/recent-workouts/', views.get_recent_workouts, name='get_recent_workouts'),
    path('progress/', views.progress, name='progress'),
    path('upload-picture/', views.upload_picture, name='upload_picture'),
    path('delete-picture/<int:pic_id>/', views.delete_picture, name='delete_picture'),
    path('delete/workout/<int:workout_id>/', views.delete_workout, name='delete_workout'),
    path('delete/meal/<int:meal_id>/', views.delete_meal, name='delete_meal'),
    
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)