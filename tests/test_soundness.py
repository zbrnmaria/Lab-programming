# tests/test_soundness.py
import unittest
from soundness_check import correct_uv

class TestUVSoundness(unittest.TestCase):
    def setUp(self):
        """Завантаження тестових текстів з файлу"""
        with open('test_texts.txt', 'r', encoding='utf-8') as f:
            # Розбиваємо на блоки текстів через порожній рядок
            self.test_texts = [block.strip() for block in f.read().split('\n\n') if block.strip()]

    def test_simple_cases(self):
        # Перевірка базових випадків
        self.assertEqual(correct_uv("Прийшов в сад"), "Прийшов у сад")
        self.assertEqual(correct_uv("Була у місті"), "Була в місті")
        self.assertEqual(correct_uv("В очах"), "В очах")  # початок речення
        self.assertEqual(correct_uv("у нього в очах"), "у нього в очах")  # коректно

    def test_exceptions(self):
        # Винятки
        self.assertEqual(correct_uv("Це вдача."), "Це вдача.")
        self.assertEqual(correct_uv("Умова важлива."), "Умова важлива.")
        self.assertEqual(correct_uv("Указ був підписаний."), "Указ був підписаний.")

    def test_prefix_cases(self):
        # Префікси
        self.assertEqual(correct_uv("ввімкнути світло"), "увімкнути світло")
        self.assertEqual(correct_uv("Вважай на мене"), "Уважай на мене")

    def test_full_texts(self):
        # Тест на повних текстах з файлу
        # Текст 1
        text1 = self.test_texts[0].split('\n',1)[-1].strip()
        expected1 = "Прийшов у сад вишневий. Була в місті тихо. В очах засяяла іскра. Зібрались у вечірній час. Ми сидимо у вагоні потяга."
        self.assertEqual(correct_uv(text1), expected1)

        # Текст 2
        text2 = self.test_texts[1].split('\n',1)[-1].strip()
        expected2 = "У нас у школі є учень, що займається у спортивній секції. Вона йшла в кімнату, щоб покласти речі. Потім узяла у нього важливий документ."
        self.assertEqual(correct_uv(text2), expected2)

        # Текст 3
        text3 = self.test_texts[2].split('\n',1)[-1].strip()
        expected3 = "Він утік у воду, а потім виліз. Вона побачила, як він утомлено йшов. Усе вказувало на те, що у нього проблеми."
        self.assertEqual(correct_uv(text3), expected3)

        # Текст 4 (винятки)
        text4 = self.test_texts[3].split('\n',1)[-1].strip()
        expected4 = "Це вдача, а не укладений план. Стоїть на видноколі мати – у неї вчись. Умова важлива."
        self.assertEqual(correct_uv(text4), expected4)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

