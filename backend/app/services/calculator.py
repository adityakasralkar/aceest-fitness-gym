PROGRAMS = {
    "Fat Loss (FL)": {
        "factor": 22,
        "description": "High intensity, caloric deficit program",
        "workouts": ["HIIT", "Circuit Training", "Cardio + Weights"],
    },
    "Muscle Gain (MG)": {
        "factor": 35,
        "description": "Strength focused, caloric surplus program",
        "workouts": ["Push/Pull/Legs", "Upper/Lower Split", "Full Body Strength"],
    },
    "Beginner (BG)": {
        "factor": 26,
        "description": "Foundation building, balanced program",
        "workouts": ["Full Body 3x/week", "Light Strength + Mobility"],
    },
}


def calculate_calories(weight: float, program: str) -> int:
    # Match programs case-insensitively and fall back to the safe Beginner plan.
    factors = {name.lower(): info["factor"] for name, info in PROGRAMS.items()}
    factor = factors.get(program.lower(), PROGRAMS["Beginner (BG)"]["factor"])
    return round(weight * factor)


def get_all_programs() -> dict:
    return PROGRAMS


def get_program(program: str) -> dict:
    if program not in PROGRAMS:
        raise ValueError(f"Invalid program: {program}")
    return PROGRAMS[program]
