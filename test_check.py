# test_check.py
from soundness_check import correct_uv_with_highlights

text = "Пішов в дім. У вікно був видно вдачу."
corrected, highlighted = correct_uv_with_highlights(text)

print("Оригінал:", text)
print("Виправлено:", corrected)
print("HTML:", highlighted)
