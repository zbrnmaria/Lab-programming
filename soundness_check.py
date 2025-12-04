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
    """Перевіряє, чи слово починається з важкого приголосного кластера"""
    w = word.lower().lstrip("«'\"")
    for starter in HARD_STARTERS:
        if w.startswith(starter):
            return True
    return False


def extract_word_base(token: str) -> str:
    """Витягує слово без пунктуації в кінці"""
    return re.sub(r'[^\w\sа-яіїєґА-ЯІЇЄҐ]+$', '', token)


def correct_uv_with_highlights(text: str):
    """Виправляє 'у/в' та повертає (виправлений текст, html з підсвіченими помилками)"""
    tokens = re.split(r'(\s+|[.,;!?—:«»()"\'\[\]{}\-]+)', text)
    corrected_tokens = []
    highlighted_tokens = []

    for i, token in enumerate(tokens):
        if not token.strip():
            corrected_tokens.append(token)
            highlighted_tokens.append(token)
            continue

        clean_token = extract_word_base(token)
        tail = token[len(clean_token):]

        # Якщо не "у" або "в" на початку слова, пропускаємо
        if not re.match(r'^[УуВв](\w*)$', clean_token):
            corrected_tokens.append(token)
            highlighted_tokens.append(token)
            continue

        prefix_char = clean_token[0]
        rest = clean_token[1:]
        target = prefix_char.lower()

        # Попереднє та наступне слово
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

        # Винятки
        if next_word.lower() in EXCEPTIONS_U or next_word.lower() in EXCEPTIONS_V:
            corrected_tokens.append(token)
            highlighted_tokens.append(token)
            continue

        should_change = False
        expected = None

        # Префіксні випадки
        if rest:
            next_char = rest[0] if rest else ''
            if target == 'у' and is_vowel(next_char):
                should_change = True
                expected = 'в'
            elif target == 'в' and (is_consonant(next_char) or starts_with_hard_cluster(rest)):
                should_change = True
                expected = 'у'

        # Прийменники
        else:
            prev_last = prev_word[-1] if prev_word else ''
            next_first = next_word[0] if next_word else ''

            # В → У
            if target == 'в':
                if ((is_consonant(prev_last) and is_consonant(next_first)) or
                    (not prev_word and next_first and is_consonant(next_first)) or
                    (next_word and starts_with_hard_cluster(next_word))):
                    should_change = True
                    expected = 'у'

            # У → В
            elif target == 'у':
                if ((prev_word and is_vowel(prev_last) and next_first and is_vowel(next_first)) or
                    (prev_word and is_vowel(prev_last) and next_first and is_consonant(next_first) and
                     not (next_word and starts_with_hard_cluster(next_word))) or
                    (not prev_word and next_first and is_vowel(next_first))):  # на початку речення перед голосним
                    should_change = True
                    expected = 'в'

        # Застосування зміни
        if should_change:
            new_prefix = expected.upper() if prefix_char.isupper() else expected
            new_clean = new_prefix + rest
            corrected_token = new_clean + tail
            tooltip = f"Мало бути: {new_clean}"
            highlighted = f'<span class="mistake" title="{tooltip}">{clean_token}</span>{tail}'
        else:
            corrected_token = token
            highlighted = token

        corrected_tokens.append(corrected_token)
        highlighted_tokens.append(highlighted)

    return "".join(corrected_tokens), "".join(highlighted_tokens)


def correct_uv(text: str) -> str:
    """Сумісність зі старим інтерфейсом"""
    corrected, _ = correct_uv_with_highlights(text)
    return corrected

