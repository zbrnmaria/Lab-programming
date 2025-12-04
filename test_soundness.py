# test_soundness.py
import pytest
from soundness_check import correct_uv_with_highlights

def test_simple_correction():
    text = "Пішов в дім."
    corrected, _ = correct_uv_with_highlights(text)
    assert corrected == "Пішов у дім."

def test_exception_v():
    # "вдача" — виняток: має лишитися "в"
    text = "Це вдача."
    corrected, _ = correct_uv_with_highlights(text)
    assert corrected == "Це вдача."  # не "удача"

def test_prefix_correction():
    text = "ввімкнути"
    corrected, _ = correct_uv_with_highlights(text)
    assert corrected == "увімкнути"  # "в" перед "в" → "у"

def test_multiple_mistakes():
    text = "Вийшов в центр у вікні."
    corrected, _ = correct_uv_with_highlights(text)
    assert corrected == "Уйшов у центр у вікні."  # "Вийшов" → "Уйшов", "в центр" → "у центр"

def test_no_change_needed():
    text = "У хаті було тепло."
    corrected, _ = correct_uv_with_highlights(text)
    assert corrected == "У хаті було тепло."  # не має змінюватися
    