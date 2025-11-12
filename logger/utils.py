# utils.py (recommended)
from math import ceil
from .models import ExerciseProgress

def update_exercise_progress(user, workout):
    """
    Aggregate workout data into ExerciseProgress entries.
    """
    for we in workout.workoutexercise_set.all():
        total_volume = (we.weight or 0) * (we.reps or 0) * (we.sets or 0)
        total_reps = (we.reps or 0) * (we.sets or 0)
        avg_weight = we.weight or 0
        one_rep_max_est = (we.weight or 0) * (1 + (we.reps or 0) / 30.0)

        progress, _ = ExerciseProgress.objects.get_or_create(
            user=user,
            exercise=we.exercise,
            date=workout.date,
            defaults={
                'total_volume': total_volume,
                'avg_weight': avg_weight,
                'total_sets': we.sets,
                'total_reps': total_reps,
                'one_rep_max_est': one_rep_max_est
            }
        )

        # If progress exists, update it
        progress.total_volume += total_volume
        progress.total_sets += we.sets
        progress.total_reps += total_reps
        progress.avg_weight = (progress.avg_weight + avg_weight) / 2
        progress.one_rep_max_est = max(progress.one_rep_max_est, one_rep_max_est)
        progress.save()
