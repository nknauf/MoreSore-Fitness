from django.db import models
from django.contrib.auth.models import User 


class MuscleGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
    
class BaseExercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    primary_muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE, related_name='primary_exercises')
    secondary_muscle_groups = models.ManyToManyField(MuscleGroup, blank=True, related_name='secondary_exercises')

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    base_exercise = models.ForeignKey(BaseExercise, on_delete=models.CASCADE, related_name="exercises")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='equipment')

    @property
    def primary_muscle_group(self):
        return self.base_exercise.primary_muscle_group 
    
    @property
    def secondary_muscle_groups(self):
        return self.base_exercise.secondary_muscle_groups.all() # Returns QuerySet

    def __str__(self):
        return self.name
    
class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()
    exercises = models.ManyToManyField(Exercise, through='WorkoutExercise')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date}"
    class Meta:
        ordering = ['-date', '-created_at']


class StageWorkout(models.Model):
    user = models.ForeignKey(User, on_delete =models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Staged Workout for {self.user.username}"

class WorkoutExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField(default=3)
    reps = models.PositiveIntegerField(default=8)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rest_seconds = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)


class ExerciseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField()
    total_volume = models.FloatField(default=0)  # sets × reps × weight
    avg_weight = models.FloatField(default=0)
    total_sets = models.IntegerField(default=0)
    total_reps = models.IntegerField(default=0)
    one_rep_max_est = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'exercise', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.exercise.name} ({self.date})"

    

class SavedWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date = models.DateField()
    exercises = models.ManyToManyField(WorkoutExercise)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.date}"
    class Meta:
        ordering = ['-date', '-created_at']

class MealEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    calories = models.PositiveIntegerField()
    protein = models.PositiveIntegerField()
    carbs = models.PositiveIntegerField(blank=True)
    fats = models.PositiveIntegerField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.calories} cal ({self.date})"
    class Meta:
        ordering = ['-date', '-created_at']

class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    workouts = models.ManyToManyField(Workout, blank=True, related_name='daily_logs')
    meals = models.ManyToManyField(MealEntry, blank=True, related_name='daily_logs')
    total_calories = models.PositiveIntegerField(default=0)
    total_protein = models.PositiveIntegerField(default=0)
    total_carbs = models.PositiveIntegerField(default=0)
    total_fats = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
class UserProfile(models.Model):
    VISIBILITY_CHOICES = (
    ("friends", "Friends"),
    ("public", "Public"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_user")
    content = models.TextField(max_length=2000)
    # Optional attachments to your existing domain objects
    workout = models.ForeignKey("Workout", null=True, blank=True, on_delete=models.SET_NULL, related_name="profile_workout")
    meal = models.ForeignKey("MealEntry", null=True, blank=True, on_delete=models.SET_NULL, related_name="profile_meal")
    visibility = models.CharField(max_length=12, choices=VISIBILITY_CHOICES, default="friends")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post by {self.author.username} @ {self.created_at:%Y-%m-%d %H:%M}"
    
class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pump_pics/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pump Pic by {self.user.username} at {self.uploaded_at:%Y-%m-%d %H:%M}"
    