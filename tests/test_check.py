from soundness_check import correct_uv_with_highlights

# Текст для тестування
text = "Пішов в дім. У вікно був видно вдачу."

# Викликаємо функцію
corrected, highlighted = correct_uv_with_highlights(text)

# Друкуємо результати
print("Оригінал:", text)
print("Виправлено:", corrected)
print("HTML:", highlighted)

# Для pytest можна додати assert, щоб зробити тест автоматичним
assert corrected == "Пішов у дім. В вікно був видно вдачу."  # або очікуваний результат

