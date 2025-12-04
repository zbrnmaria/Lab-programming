# soundness_check.py
import re

# Набори літер
CONSONANTS = set("бвгґджзклмнпрстфхцчшщй")
VOWELS = set("аеиіоуюяєї")
HARD_STARTERS = {
    'в', 'ф', 'ль', 'св', 'тв', 'хв', 'зв', 'дв', 'жв', 'цв', 'чв', 'шв', 'щв'
}
# Слова, які *завжди* пишуться з "у"
EXCEPTIONS_U = {
    "увага", "ударник", "узбережжя", "указ", "умова", "усталення", 
    "установа", "уява", "університет", "успіх", "уклад"
}
# Слова, які *завжди* пишуться з "в"
EXCEPTIONS_V = {
    "вдача", "вклад", "вправа", "вступ", "взаємини", "влада", "власний",
    "властивість", "вплив", "відповідь", "вихід", "вигляд", "відомість"
}

def is_vowel(ch: str) -> bool:
    return ch.lower() in VOWELS

def is_consonant(ch: str) -> bool:
    return ch.lower() in CONSONANTS

def starts_with_hard_cluster(word: str) -> bool:
    """Перевіряє, чи слово починається з 'в', 'ф', 'ль', 'св', 'тв', 'хв' тощо."""
    w = word.lower().lstrip("«'\"")  # прибираємо ліві лапки/апострофи
    for starter in HARD_STARTERS:
        if w.startswith(starter):
            return True
    return False

def extract_word_base(token: str) -> str:
    """Витягує слово, прибираючи пунктуацію (наприклад, 'у!' → 'у')."""
    # Видаляємо пунктуацію з кінця (не з початку — важливо для "у!")
    return re.sub(r'[^\w\sа-яіїєґА-ЯІЇЄҐ]+$', '', token)

def correct_uv_with_highlights(text: str):
    """
    Виправляє 'у/в' і повертає:
        (виправлений_текст: str, html_з_підсвічуванням_помилок: str)
    """
    tokens = re.split(r'(\s+|[.,;!?—:«»()"\'\[\]{}\-]+)', text)
    corrected_tokens = []
    highlighted_tokens = []

    for i, token in enumerate(tokens):
        if not token.strip():
            corrected_tokens.append(token)
            highlighted_tokens.append(token)
            continue

        # Витягуємо чисте слово для аналізу (без пунктуації в кінці)
        clean_token = extract_word_base(token)
        tail = token[len(clean_token):]  # пунктуація в кінці: '!', ',', '...' тощо

        # Шукаємо 'у'/'в' на початку слова (префікс або прийменник)
        is_prefix_or_prep = re.match(r'^[УуВв](\w*)$', clean_token)
        if not is_prefix_or_prep:
            corrected_tokens.append(token)
            highlighted_tokens.append(token)
            continue

        prefix_char = clean_token[0]  # 'У', 'у', 'В', 'в'
        rest = clean_token[1:]
        target = prefix_char.lower()

        # Визначаємо попереднє та наступне *чисте* слово
        prev_word = ""
        for j in range(i - 1, -1, -1):
            candidate = extract_word_base(tokens[j])
            if candidate and re.match(r'^[а-яіїєґА-ЯІЇЄҐ]+$', candidate):
                prev_word = candidate
                break

        next_word = ""
        for j in range(i + 1, len(tokens)):
            candidate = extract_word_base(tokens[j])
            if candidate and re.match(r'^[а-яіїєґА-ЯІЇЄҐ]+$', candidate):
                next_word = candidate
                break

        #  Перевірка винятків 
        full_next = next_word.lower()
        if full_next in EXCEPTIONS_U or full_next in EXCEPTIONS_V:
            corrected_tokens.append(token)
            highlighted_tokens.append(token)
            continue

        #  Логіка виправлення 
        should_change = False
        expected = None  # 'у' або 'в'

        # 1. Для префіксів (rest не порожній)
        if rest:
            next_char = rest[0] if rest else ''
            # У → В перед голосною
            if target == 'у' and is_vowel(next_char):
                should_change = True
                expected = 'в'
            # В → У перед приголосною або "важким" початком
            elif target == 'в' and (is_consonant(next_char) or starts_with_hard_cluster(rest)):
                should_change = True
                expected = 'у'

        # 2. Для прийменників (rest порожній → саме "у"/"в")
        else:
            prev_last = prev_word[-1] if prev_word else ''
            next_first = next_word[0] if next_word else ''

            if target == 'в':
                # В → У, якщо:
                # - після приголосного + перед приголосною
                # - на початку речення перед приголосною
                # - перед "важким" початком
                if ((is_consonant(prev_last) and is_consonant(next_first)) or
                    (not prev_word and is_consonant(next_first)) or
                    (next_word and starts_with_hard_cluster(next_word))):
                    should_change = True
                    expected = 'у'

            elif target == 'у':
                # У → В, якщо:
                # - після голосного + перед голосною
                # - після голосного + перед приголосною (якщо не "важка")
                if ((is_vowel(prev_last) and is_vowel(next_first)) or
                    (is_vowel(prev_last) and is_consonant(next_first) and 
                     not (next_word and starts_with_hard_cluster(next_word)))):
                    should_change = True
                    expected = 'в'

        # Застосування змін 
        if should_change:
            new_prefix = expected.upper() if prefix_char.isupper() else expected
            new_clean = new_prefix + rest
            corrected_token = new_clean + tail

            # Підсвічування: <span class="mistake" title="Мало бути: ХХХ">оригінал</span>
            tooltip = f"Мало бути: {new_clean}"
            highlighted = f'<span class="mistake" title="{tooltip}">{clean_token}</span>{tail}'
        else:
            corrected_token = token
            highlighted = token

        corrected_tokens.append(corrected_token)
        highlighted_tokens.append(highlighted)

    return "".join(corrected_tokens), "".join(highlighted_tokens)


# Совместимість зі старим інтерфейсом (якщо десь використовується `correct_uv`)
def correct_uv(text: str) -> str:
    corrected, _ = correct_uv_with_highlights(text)
    return corrected
