from django.db import transaction
from .models import Equipment, Exercise, MuscleGroup, BaseExercise

@transaction.atomic
def run():

    if MuscleGroup.objects.exists():
        print("⚠️ MuscleGroups already exist. Run clear_data() first or skip seeding.")
        return
    
    # 1. Create BaseMuscle & Muscles
    base_muscles_data = [
        {"name": "Chest", "muscles": ["UpperChest", "MidChest", "LowerChest"]},
        {"name": "Back", "muscles": ["UpperBack", "Lats", "LowerBack"]},
        {"name": "Shoulders", "muscles": ["FrontDelt", "SideDelt", "RearDelt"]},
        {"name": "Arms", "muscles": ["Biceps", "Triceps", "Forearms"]},
        {"name": "Legs", "muscles": ["Quads", "Hamstrings", "Glutes", "Calves", "Adductors", "Abductors"]},
        {"name": "Core", "muscles": ["Abs", "Obliques"]},
    ]
    
    muscle_group_objs = {}
    for base_muscle_data in base_muscles_data:
        base_name = base_muscle_data["name"]
        base_muscle, _ = MuscleGroup.objects.get_or_create(name=base_name)
        muscle_group_objs[base_name] = base_muscle
        for muscle_name in base_muscle_data["muscles"]:
            muscle, _ = MuscleGroup.objects.get_or_create(name=muscle_name)
            muscle_group_objs[muscle_name] = muscle
    
    print("Created all muscle groups successfully!")

    # 2. Create Equipment
    equipment_data = [
        "Barbell", "Dumbbell", "Cable", "Machine", "Smith", "EZBar", "FlatBar", "PullUpBar", "Bodyweight",
    ]
    
    equipment_objs = {}
    for equipment_name in equipment_data:
        equipment = Equipment.objects.create(name=equipment_name)
        equipment_objs[equipment_name] = equipment
    
    print("Created equipment successfully!")

    exercises = [
        # {"name": "Bench Press", "primary_muscle_group": "Chest", "secondary_muscle_groups": ["FrontDelt", "Triceps"], "exercises":
        #  [
        #   {"name": "Barbell Bench Press", "base_exercise": "Bench Press", "equipment": "Barbell"},
        #   {"name": "Dumbbell Bench Press", "base_exercise": "Bench Press", "equipment": "Dumbbell"}
        #  ]
        #  },
        # {"name": "Chest Fly", "primary_muscle_group": "Chest", "secondary_muscle_groups": "", "exercises" :
        #  [
        #   {"name": "Pec Deck", "base_exercise": "Chest Fly", "equipment": "Machine"},
        #   {"name": "Seated Cable Chest Fly", "base_exercise": "Chest Fly", "equipment": "Cable"},
        #   ]
        #   },
        {
        "name": "Bench Press",
        "primary_muscle_group": "Chest",
        "secondary_muscle_groups": ["FrontDelt", "Triceps"],
        "exercises": [
            {"name": "Barbell Bench Press", "base_exercise": "Bench Press", "equipment": "Barbell"},
            {"name": "Dumbbell Bench Press", "base_exercise": "Bench Press", "equipment": "Dumbbell"},
            {"name": "Smith Machine Bench Press", "base_exercise": "Bench Press", "equipment": "Smith"},
            {"name": "PlateLoaded Chest Press", "base_exercise": "Bench Press", "equipment": "Machine"},
            {"name": "PinLoaded Chest Press", "base_exercise": "Bench Press", "equipment": "Machine"},
        ]
        },
        {
        "name": "Incline Chest Press",
        "primary_muscle_group": "Chest",
        "secondary_muscle_groups": ["FrontDelt", "Triceps"],
        "exercises": [
            {"name": "Barbell Incline Chest Press", "base_exercise": "Incline Chest Press", "equipment": "Barbell"},
            {"name": "Dumbbell Incline Chest Press", "base_exercise": "Incline Chest Press", "equipment": "Dumbbell"},
            {"name": "Smith Machine Incline Chest Press", "base_exercise": "Incline Chest Press", "equipment": "Smith"},
            {"name": "PlateLoaded Incline Chest Press", "base_exercise": "Incline Chest Press", "equipment": "Machine"},
            {"name": "PinLoaded Incline Chest Press", "base_exercise": "Incline Chest Press", "equipment": "Machine"},
        ]
        },
        {
        "name": "Decline Chest Press",
        "primary_muscle_group": "Chest",
        "secondary_muscle_groups": ["Triceps"],
        "exercises": [
            {"name": "Barbell Decline Chest Press", "base_exercise": "Decline Chest Press", "equipment": "Barbell"},
            {"name": "Dumbbell Decline Chest Press", "base_exercise": "Decline Chest Press", "equipment": "Dumbbell"},
            {"name": "Smith Machine Decline Chest Press", "base_exercise": "Decline Chest Press", "equipment": "Smith"},
            {"name": "PlateLoaded Decline Chest Press", "base_exercise": "Decline Chest Press", "equipment": "Machine"},
            {"name": "PinLoaded Decline Chest Press", "base_exercise": "Decline Chest Press", "equipment": "Machine"},
        ]
        },
        {
        "name": "Chest Fly",
        "primary_muscle_group": "Chest",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "Dumbbell Chest Fly", "base_exercise": "Chest Fly", "equipment": "Dumbbell"},
            {"name": "Cable Chest Fly", "base_exercise": "Chest Fly", "equipment": "Cable"},
            {"name": "PlateLoaded Chest Fly", "base_exercise": "Chest Fly", "equipment": "Machine"},
            {"name": "Pec Deck", "base_exercise": "Chest Fly", "equipment": "Machine"},
        ]
        },
        {
        "name": "Incline Chest Fly",
        "primary_muscle_group": "Chest",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "Dumbbell Incline Chest Fly", "base_exercise": "Incline Chest Fly", "equipment": "Dumbbell"},
            {"name": "Cable Incline Chest Fly", "base_exercise": "Incline Chest Fly", "equipment": "Cable"},
            {"name": "PlateLoaded Incline Chest Fly", "base_exercise": "Incline Chest Fly", "equipment": "Machine"},
            {"name": "PinLoaded Incline Chest Fly", "base_exercise": "Incline Chest Fly", "equipment": "Machine"},
        ]
        },
        {
        "name": "Decline Chest Fly",
        "primary_muscle_group": "Chest",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "Dumbbell Decline Chest Fly", "base_exercise": "Decline Chest Fly", "equipment": "Dumbbell"},
            {"name": "Cable Decline Chest Fly", "base_exercise": "Decline Chest Fly", "equipment": "Cable"},
            {"name": "PlateLoaded Decline Chest Fly", "base_exercise": "Decline Chest Fly", "equipment": "Machine"},
            {"name": "PinLoaded Decline Chest Fly", "base_exercise": "Decline Chest Fly", "equipment": "Machine"},
        ]
        },
        {
        "name": "Push Up",
        "primary_muscle_group": "Chest",
        "secondary_muscle_groups": ["Triceps"],
        "exercises": [
            {"name": "Bodyweight Push Up", "base_exercise": "Push Up", "equipment": "Bodyweight"},
            {"name": "Incline Push Up", "base_exercise": "Push Up", "equipment": "Bodyweight"},
            {"name": "Decline Push Up", "base_exercise": "Push Up", "equipment": "Bodyweight"},
        ]
        },
        {
        "name": "Dips",
        "primary_muscle_group": "Triceps",
        "secondary_muscle_groups": ["LowerChest"],
        "exercises": [
            {"name": "Bodyweight Dips", "base_exercise": "Dips", "equipment": "Bodyweight"},
            {"name": "Weighted Dips", "base_exercise": "Dips", "equipment": "Bodyweight"},
            {"name": "Machine Dips", "base_exercise": "Dips", "equipment": "Machine"},
        ]
        },
        {
        "name": "Pull Up",
        "primary_muscle_group": "Back",
        "secondary_muscle_groups": ["Biceps", "Forearms"],
        "exercises": [
            {"name": "Bodyweight Pull Up", "base_exercise": "Pull Up", "equipment": "Bodyweight"},
            {"name": "Weighted Pull Up", "base_exercise": "Pull Up", "equipment": "Bodyweight"},
            {"name": "Assisted Pull Up", "base_exercise": "Pull Up", "equipment": "Machine"},
        ]
        },
        {
        "name": "Lat Pulldown",
        "primary_muscle_group": "Back",
        "secondary_muscle_groups": ["Biceps", "Forearms"],
        "exercises": [
            {"name": "Cable Lat Pulldown", "base_exercise": "Lat Pulldown", "equipment": "Cable"},
            {"name": "PlateLoaded Lat Pulldown", "base_exercise": "Lat Pulldown", "equipment": "Machine"},
            {"name": "PinLoaded Lat Pulldown", "base_exercise": "Lat Pulldown", "equipment": "Machine"},
        ]
        },
        {
        "name": "Row",
        "primary_muscle_group": "Back",
        "secondary_muscle_groups": ["Biceps", "Forearms"],
        "exercises": [
            {"name": "Barbell Row", "base_exercise": "Row", "equipment": "Barbell"},
            {"name": "Dumbbell Row", "base_exercise": "Row", "equipment": "Dumbbell"},
            {"name": "Cable Row", "base_exercise": "Row", "equipment": "Cable"},
            {"name": "PlateLoaded Row", "base_exercise": "Row", "equipment": "Machine"},
            {"name": "PinLoaded Row", "base_exercise": "Row", "equipment": "Machine"},
            {"name": "Smith Machine Row", "base_exercise": "Row", "equipment": "Smith"},
            {"name": "PlateLoaded T-Bar Row", "base_exercise": "Row", "equipment": "Machine"},
            {"name": "Landmine Row", "base_exercise": "Row", "equipment": "Barbell"},
        ]
        },
        {
        "name": "Deadlift",
        "primary_muscle_group": "Back",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "Barbell Deadlift", "base_exercise": "Deadlift", "equipment": "Barbell"},
            {"name": "Dumbbell Deadlift", "base_exercise": "Deadlift", "equipment": "Dumbbell"},
            {"name": "Smith Machine Deadlift", "base_exercise": "Deadlift", "equipment": "Smith"},
            {"name": "Trap Bar Deadlift", "base_exercise": "Deadlift", "equipment": "Barbell"},
        ]
        },
        {
        "name": "Shrug",
        "primary_muscle_group": "Back",
        "secondary_muscle_groups": ["UpperBack"],
        "exercises": [
            {"name": "Barbell Shrug", "base_exercise": "Shrug", "equipment": "Barbell"},
            {"name": "Dumbbell Shrug", "base_exercise": "Shrug", "equipment": "Dumbbell"},
            {"name": "Smith Machine Shrug", "base_exercise": "Shrug", "equipment": "Smith"},
            {"name": "PlateLoaded Shrug", "base_exercise": "Shrug", "equipment": "Machine"},
            {"name": "PinLoaded Shrug", "base_exercise": "Shrug", "equipment": "Machine"},
        ]
        },
        {
        "name": "Shoulder Press",
        "primary_muscle_group": "Shoulders",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "Barbell Shoulder Press", "base_exercise": "Shoulder Press", "equipment": "Barbell"},
            {"name": "Dumbbell Shoulder Press", "base_exercise": "Shoulder Press", "equipment": "Dumbbell"},
            {"name": "Smith Machine Shoulder Press", "base_exercise": "Shoulder Press", "equipment": "Smith"},
            {"name": "PlateLoaded Shoulder Press", "base_exercise": "Shoulder Press", "equipment": "Machine"},
            {"name": "PinLoaded Shoulder Press", "base_exercise": "Shoulder Press", "equipment": "Machine"},
        ]
        },
        {
        "name": "Lat Raise",
        "primary_muscle_group": "Shoulders",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "Dumbbell Lat Raise", "base_exercise": "Lat Raise", "equipment": "Dumbbell"},
            {"name": "Cable Lat Raise", "base_exercise": "Lat Raise", "equipment": "Cable"},
            {"name": "PlateLoaded Lat Raise", "base_exercise": "Lat Raise", "equipment": "Machine"},
            {"name": "PinLoaded Lat Raise", "base_exercise": "Lat Raise", "equipment": "Machine"},
        ]
        },
        {
        "name": "Reverse Fly",
        "primary_muscle_group": "RearDelt",
        "secondary_muscle_groups": ["UpperBack"],
        "exercises": [
            {"name": "Dumbbell Reverse Fly", "base_exercise": "Reverse Fly", "equipment": "Dumbbell"},
            {"name": "Cable Reverse Fly", "base_exercise": "Reverse Fly", "equipment": "Cable"},
            {"name": "Reverse Pec Deck", "base_exercise": "Reverse Fly", "equipment": "Machine"},
            {"name": "Rear Delt PlateLoaded Machine Fly", "base_exercise": "Reverse Fly", "equipment": "Machine"},
            {"name": "Bent-over Rear Delt Raise", "base_exercise": "Reverse Fly", "equipment": "Barbell"},
        ]
        },
        {
        "name": "Y Raise",
        "primary_muscle_group": "Shoulders",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "Dumbbell Y Raise", "base_exercise": "Y Raise", "equipment": "Dumbbell"},
            {"name": "Cable Y Raise", "base_exercise": "Y Raise", "equipment": "Cable"},
        ]
        },
        {
        "name": "Curl",
        "primary_muscle_group": "Biceps",
        "secondary_muscle_groups": ["Forearms"],
        "exercises": [
            {"name": "Barbell Curl", "base_exercise": "Curl", "equipment": "Barbell"},
            {"name": "EZBar Curl", "base_exercise": "Curl", "equipment": "EZBar"},
            {"name": "Dumbbell Curl", "base_exercise": "Curl", "equipment": "Dumbbell"},
            {"name": "Cable Curl", "base_exercise": "Curl", "equipment": "Cable"},
            {"name": "PlateLoaded Machine Curl", "base_exercise": "Curl", "equipment": "Machine"},
            {"name": "PinLoaded Machine Curl", "base_exercise": "Curl", "equipment": "Machine"},
            {"name": "PlateLoaded Preacher Curl", "base_exercise": "Curl", "equipment": "Machine"},
            {"name": "PinLoaded Preacher Curl", "base_exercise": "Curl", "equipment": "Machine"},
            {"name": "Dumbbell Preacher Curl", "base_exercise": "Curl", "equipment": "Dumbbell"},
            {"name": "Incline Dumbbell Curl", "base_exercise": "Curl", "equipment": "Dumbbell"},
            {"name": "Zottman Curl", "base_exercise": "Curl", "equipment": "Dumbbell"},
            {"name": "Dumbbell Spider Curl", "base_exercise": "Curl", "equipment": "Dumbbell"},
            {"name": "EZBar Spider Curl", "base_exercise": "Curl", "equipment": "EZBar"},
            {"name": "Dumbbell Drag Curl", "base_exercise": "Curl", "equipment": "Dumbbell"},
            {"name": "Cable Drag Curl", "base_exercise": "Curl", "equipment": "Cable"},
            {"name": "Cable Bayesian Curl", "base_exercise": "Curl", "equipment": "Cable"},
        ]
        },
        {
        "name": "Chin Up",
        "primary_muscle_group": "Biceps",
        "secondary_muscle_groups": ["Lats"],
        "exercises": [
            {"name": "Bodyweight Chin Up", "base_exercise": "Chin Up", "equipment": "Bodyweight"},
            {"name": "Cable Chin Up", "base_exercise": "Chin Up", "equipment": "Cable"},
        ]
        },
        {
        "name": "Tricep Extension",
        "primary_muscle_group": "Triceps",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "PlateLoaded Tricep Extension", "base_exercise": "Tricep Extension", "equipment": "Machine"},
            {"name": "PinLoaded Tricep Extension", "base_exercise": "Tricep Extension", "equipment": "Machine"},
            {"name": "Overhead Dumbbell Tricep Extension", "base_exercise": "Tricep Extension", "equipment": "Dumbbell"},
            {"name": "EZBar Tricep Skullcrusher", "base_exercise": "Tricep Extension", "equipment": "EZBar"},
            {"name": "FlatBar Tricep Skullcrusher", "base_exercise": "Tricep Extension", "equipment": "Barbell"},
            {"name": "Dumbbell Tricep Skullcrusher", "base_exercise": "Tricep Extension", "equipment": "Dumbbell"},
            {"name": "Cable Tricep Skullcrusher", "base_exercise": "Tricep Extension", "equipment": "Cable"},
            {"name": "Cross Cable Tricep Extensions", "base_exercise": "Tricep Extension", "equipment": "Cable"},
            {"name": "Dumbbell Tricep Kickbacks", "base_exercise": "Tricep Extension", "equipment": "Dumbbell"},
            {"name": "Cable Tricep Kickbacks", "base_exercise": "Tricep Extension", "equipment": "Cable"},
        ]
        },
        {
        "name": "Tricep Pushdown",
        "primary_muscle_group": "Triceps",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "PinLoaded Tricep Pushdown", "base_exercise": "Tricep Pushdown", "equipment": "Machine"},
            {"name": "PlateLoaded Tricep Pushdown", "base_exercise": "Tricep Pushdown", "equipment": "Machine"},
            {"name": "Cable Tricep Pushdown", "base_exercise": "Tricep Pushdown", "equipment": "Cable"},
        ]
        },
        {
        "name": "JM Press",
        "primary_muscle_group": "Triceps",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "Barbell JM Press", "base_exercise": "JM Press", "equipment": "Barbell"},
            {"name": "Dumbbell JM Press", "base_exercise": "JM Press", "equipment": "Dumbbell"},
            {"name": "Smith Machine JM Press", "base_exercise": "JM Press", "equipment": "Smith"},
            {"name": "Machine JM Press", "base_exercise": "JM Press", "equipment": "Machine"},
        ]
        },
        {
        "name": "Reverse Curl",
        "primary_muscle_group": "Forearms",
        "secondary_muscle_groups": ["Biceps"],
        "exercises": [
            {"name": "Reverse EZBar Curl", "base_exercise": "Reverse Curl", "equipment": "EZBar"},
            {"name": "Reverse FlatBar Curl", "base_exercise": "Reverse Curl", "equipment": "Barbell"},
            {"name": "Reverse Dumbbell Curl", "base_exercise": "Reverse Curl", "equipment": "Dumbbell"},
        ]
        },
        {
        "name": "Leg Extension",
        "primary_muscle_group": "Quads",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "PlateLoaded Leg Extensions", "base_exercise": "Leg Extension", "equipment": "Machine"},
            {"name": "PinLoaded Leg Extensions", "base_exercise": "Leg Extension", "equipment": "Machine"},
        ]
        },
        {
        "name": "Sissy Squat",
        "primary_muscle_group": "Quads",
        "secondary_muscle_groups": ["Glutes"],
        "exercises": [
            {"name": "Bodyweight Sissy Squat", "base_exercise": "Sissy Squat", "equipment": "Bodyweight"},
            {"name": "Weighted Sissy Squat", "base_exercise": "Sissy Squat", "equipment": "Barbell"},
            {"name": "Smith Machine Sissy Squat", "base_exercise": "Sissy Squat", "equipment": "Smith"},
            {"name": "Hacksquat Sissy Squat", "base_exercise": "Sissy Squat", "equipment": "Machine"},
        ]
        },
        {
        "name": "Front Squat",
        "primary_muscle_group": "Quads",
        "secondary_muscle_groups": ["Glutes", "Hamstrings"],
        "exercises": [
            {"name": "Barbell Front Squat", "base_exercise": "Front Squat", "equipment": "Barbell"},
            {"name": "Dumbbell Front Squat", "base_exercise": "Front Squat", "equipment": "Dumbbell"},
            {"name": "Smith Machine Front Squat", "base_exercise": "Front Squat", "equipment": "Smith"},
            {"name": "Goblet Squat", "base_exercise": "Front Squat", "equipment": "Dumbbell"},
        ]
        },
        {
        "name": "Leg Curl",
        "primary_muscle_group": "Hamstrings",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "Lying PlateLoaded Leg Curl", "base_exercise": "Leg Curl", "equipment": "Machine"},
            {"name": "Lying PinLoaded Leg Curl", "base_exercise": "Leg Curl", "equipment": "Machine"},
            {"name": "PlateLoaded Leg Curl", "base_exercise": "Leg Curl", "equipment": "Machine"},
            {"name": "PinLoaded Leg Curl", "base_exercise": "Leg Curl", "equipment": "Machine"},
            {"name": "Standing Leg Curl", "base_exercise": "Leg Curl", "equipment": "Machine"},
            {"name": "Cable Leg Curl", "base_exercise": "Leg Curl", "equipment": "Cable"},
        ]
        },
        {
        "name": "RDL",
        "primary_muscle_group": "Hamstrings",
        "secondary_muscle_groups": ["Glutes"],
        "exercises": [
            {"name": "Barbell RDL", "base_exercise": "RDL", "equipment": "Barbell"},
            {"name": "Dumbbell RDL", "base_exercise": "RDL", "equipment": "Dumbbell"},
            {"name": "Smith Machine RDL", "base_exercise": "RDL", "equipment": "Smith"},
            {"name": "PlateLoaded RDL", "base_exercise": "RDL", "equipment": "Machine"},
            {"name": "PinLoaded RDL", "base_exercise": "RDL", "equipment": "Machine"},
        ]
        },
        {
        "name": "Hip Thrust",
        "primary_muscle_group": "Glutes",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "Barbell Hip Thrust", "base_exercise": "Hip Thrust", "equipment": "Barbell"},
            {"name": "Dumbbell Hip Thrust", "base_exercise": "Hip Thrust", "equipment": "Dumbbell"},
            {"name": "Smith Machine Hip Thrust", "base_exercise": "Hip Thrust", "equipment": "Smith"},
            {"name": "PlateLoaded Hip Thrust", "base_exercise": "Hip Thrust", "equipment": "Machine"},
            {"name": "PinLoaded Hip Thrust", "base_exercise": "Hip Thrust", "equipment": "Machine"},
        ]
        },
        {
        "name": "Glute Kickback",
        "primary_muscle_group": "Glutes",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "Cable Glute Kickback", "base_exercise": "Glute Kickback", "equipment": "Cable"},
            {"name": "PlateLoaded Glute Kickback", "base_exercise": "Glute Kickback", "equipment": "Machine"},
            {"name": "PinLoaded Glute Kickback", "base_exercise": "Glute Kickback", "equipment": "Machine"},
        ]
        },
        {
        "name": "Glute Bridge",
        "primary_muscle_group": "Glutes",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "Bodyweight Glute Bridge", "base_exercise": "Glute Bridge", "equipment": "Bodyweight"},
            {"name": "Barbell Glute Bridge", "base_exercise": "Glute Bridge", "equipment": "Barbell"},
            {"name": "Dumbbell Glute Bridge", "base_exercise": "Glute Bridge", "equipment": "Dumbbell"},
        ]
        },
        {
        "name": "Calf Raise",
        "primary_muscle_group": "Calves",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "Barbell Calf Raise", "base_exercise": "Calf Raise", "equipment": "Barbell"},
            {"name": "Dumbbell Calf Raise", "base_exercise": "Calf Raise", "equipment": "Dumbbell"},
            {"name": "PlateLoaded Calf Raise", "base_exercise": "Calf Raise", "equipment": "Machine"},
            {"name": "PinLoaded Calf Raise", "base_exercise": "Calf Raise", "equipment": "Machine"},
            {"name": "Seated PlateLoaded Calf Raise", "base_exercise": "Calf Raise", "equipment": "Machine"},
            {"name": "Seated PinLoaded Calf Raise", "base_exercise": "Calf Raise", "equipment": "Machine"},
            {"name": "Smith Machine Calf Raise", "base_exercise": "Calf Raise", "equipment": "Smith"},
        ]
        },
        {
        "name": "Adduction Machine",
        "primary_muscle_group": "Adductors",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "PinLoaded Adduction Machine", "base_exercise": "Adduction Machine", "equipment": "Machine"},
            {"name": "PlateLoaded Adduction Machine", "base_exercise": "Adduction Machine", "equipment": "Machine"},
        ]
        },
        {
        "name": "Abduction Machine",
        "primary_muscle_group": "Abductors",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "PinLoaded Abduction Machine", "base_exercise": "Abduction Machine", "equipment": "Machine"},
            {"name": "PlateLoaded Abduction Machine", "base_exercise": "Abduction Machine", "equipment": "Machine"},
        ]
        },
        {
        "name": "Squat",
        "primary_muscle_group": "Legs",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "Barbell Back Squat", "base_exercise": "Squat", "equipment": "Barbell"},
            {"name": "Barbell Front Squat", "base_exercise": "Squat", "equipment": "Barbell"},
            {"name": "Dumbbell Squat", "base_exercise": "Squat", "equipment": "Dumbbell"},
            {"name": "Goblet Squat", "base_exercise": "Squat", "equipment": "Dumbbell"},
            {"name": "Smith Machine Squat", "base_exercise": "Squat", "equipment": "Smith"},
            {"name": "Zercher Squat", "base_exercise": "Squat", "equipment": "Barbell"},
            {"name": "Hack Squat", "base_exercise": "Squat", "equipment": "Machine"},
            {"name": "Trap Bar Squat", "base_exercise": "Squat", "equipment": "Barbell"},
        ]
        },
        {
        "name": "Lunge",
        "primary_muscle_group": "Legs",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "Bodyweight Lunge", "base_exercise": "Lunge", "equipment": "Bodyweight"},
            {"name": "Dumbbell Lunge", "base_exercise": "Lunge", "equipment": "Dumbbell"},
            {"name": "Barbell Lunge", "base_exercise": "Lunge", "equipment": "Barbell"},
            {"name": "Dumbbell Bulgarian Split Squat", "base_exercise": "Lunge", "equipment": "Dumbbell"},
            {"name": "Barbell Bulgarian Split Squat", "base_exercise": "Lunge", "equipment": "Barbell"},
            {"name": "Smith Machine Bulgarian Split Squat", "base_exercise": "Lunge", "equipment": "Smith"},
            {"name": "Smith Machine Lunge", "base_exercise": "Lunge", "equipment": "Smith"},
        ]
        },
        {
        "name": "Leg Press",
        "primary_muscle_group": "Legs",
        "secondary_muscle_groups": [],
        "exercises": [
            {"name": "PinLoaded Leg Press", "base_exercise": "Leg Press", "equipment": "Machine"},
            {"name": "PlateLoaded Leg Press", "base_exercise": "Leg Press", "equipment": "Machine"},
        ]
        },
    ] # end of exercise list


    created_base_exercises = {}
    created_exercises = {}

    for base_exercise in exercises:
        base_exercise_primary = base_exercise["primary_muscle_group"]
        base_exercise_secondary = base_exercise["secondary_muscle_groups"]

        if base_exercise["name"] not in created_base_exercises:
            base_ex, created = BaseExercise.objects.get_or_create(
                name = base_exercise["name"],
                defaults={"primary_muscle_group": muscle_group_objs[base_exercise_primary]}
                )
            if base_exercise_secondary:
                base_ex.secondary_muscle_groups.set([muscle_group_objs[m] for m in base_exercise_secondary])

            created_base_exercises[base_exercise["name"]] = base_ex
            base_ex.save()
        else:
            base_ex = created_base_exercises[base_exercise["name"]]

        for ex in base_exercise["exercises"]:
            ex_equipment = ex["equipment"]
            if ex["name"] not in created_exercises:
                ex_obj, created = Exercise.objects.get_or_create(
                    name = ex["name"],
                    defaults={"base_exercise": base_ex, "equipment": equipment_objs[ex_equipment]}
                    )
                created_exercises[ex["name"]] = ex_obj
                ex_obj.save()
            else:
                ex_obj = created_exercises[ex["name"]]
    
    print(f"Created {len(created_base_exercises)} base exercises and {len(exercises)} specific exercises successfully!")

@transaction.atomic
def clear_data():
    from .models import MuscleGroup, Equipment, BaseExercise, Exercise
    MuscleGroup.objects.all().delete()
    Equipment.objects.all().delete()
    BaseExercise.objects.all().delete()
    Exercise.objects.all().delete()
    print("All data deleted")