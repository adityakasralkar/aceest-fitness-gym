import pytest
from app.services.calculator import calculate_calories, get_all_programs, get_program


def test_calculate_calories_fat_loss():
    assert calculate_calories(75, "Fat Loss (FL)") == 1650


def test_calculate_calories_muscle_gain():
    assert calculate_calories(80, "Muscle Gain (MG)") == 2800


def test_calculate_calories_beginner():
    assert calculate_calories(70, "Beginner (BG)") == 1820


def test_calculate_calories_invalid_program():
    with pytest.raises(ValueError):
        calculate_calories(75, "Invalid Program")


def test_get_all_programs_returns_three():
    programs = get_all_programs()
    assert len(programs) == 3


def test_get_program_valid():
    program = get_program("Fat Loss (FL)")
    assert program["factor"] == 22


def test_get_program_invalid():
    with pytest.raises(ValueError):
        get_program("Invalid Program")