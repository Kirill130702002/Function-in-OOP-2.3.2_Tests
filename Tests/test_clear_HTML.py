from unittest import TestCase, main
from function_in_OOP import Vacancy


class ClearHTMLTest(TestCase):
    """
    Тестирование декоратора clearHTML
    """

    def test_clear_HTML_clean_line(self):
        """
        Проверяет соответствие вводимого и выводимого аргумента длиной в одно слово без html-тегов
        :return:
        """
        self.assertEqual(Vacancy.clearHTML("ОБЯЗАННОСТИ:"), "ОБЯЗАННОСТИ:")

    def test_clear_HTML_one_word(self):
        """
        Проверяет соответствие вводимого и выводимого аргумента длиной в одно слово
        :return: ничего
        """
        self.assertEqual(Vacancy.clearHTML("<p><strong>ОБЯЗАННОСТИ:</strong></p>"), "ОБЯЗАННОСТИ:")

    def test_clear_HTML_many_words(self):
        """
        Проверяет соответствие вводимого и выводимого аргумента длиной в несколько слов
        :return:
        """
        self.assertEqual(Vacancy.clearHTML("<p><strong>Cotvec </strong>- IT-компания, "
                                           "которая занимается консалтингом и разработкой программного обеспечения "
                                           "для организаций банковско-финансового сектора.</p>"),
                         "Cotvec - IT-компания, которая занимается консалтингом и разработкой программного обеспечения "
                         "для организаций банковско-финансового сектора.")


if __name__ == 'main':
    main()