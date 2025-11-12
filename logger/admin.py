from django.contrib import admin
from .models import (
    MuscleGroup, Equipment, Exercise, Workout, WorkoutExercise, 
    MealEntry, DailyLog, BaseExercise, SavedWorkout, UserProfile
)


# Register your models here.

@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1


@admin.register(BaseExercise)
class BaseExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "primary_muscle_group_display")
    search_fields = ("name", "primary_muscle_group__name")
    list_filter = ("primary_muscle_group",)
    inlines = [ExerciseInline]

    def primary_muscle_group_display(self, obj):
        return obj.primary_muscle_group.name
    primary_muscle_group_display.short_description = "Primary Muscle"


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "base_exercise", "equipment")
    search_fields = ("name", "base_exercise__name", "equipment__name")
    list_filter = ("equipment",)


class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "date", "created_at")
    search_fields = ("name", "user__username")
    list_filter = ("date", "user")
    inlines = [WorkoutExerciseInline]


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "workout", "exercise", "sets", "reps", "weight", "order")
    search_fields = ("name", "exercise__name", "user__username")
    list_filter = ("user", "workout")


@admin.register(SavedWorkout)
class SavedWorkoutAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "date", "created_at")
    search_fields = ("name", "user__username")
    list_filter = ("date", "user")


@admin.register(MealEntry)
class MealEntryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "calories", "protein", "carbs", "fats", "date")
    search_fields = ("name", "user__username")
    list_filter = ("date", "user")
    ordering = ("-date",)


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = (
        "user", "date",
        "total_calories", "total_protein", "total_carbs", "total_fats"
    )
    search_fields = ("user__username",)
    list_filter = ("date", "user")
    ordering = ("-date",)
