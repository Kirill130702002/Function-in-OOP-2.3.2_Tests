from unittest import TestCase, main
from function_in_OOP import Vacancy


class VacancyInitTest(TestCase):
    """
    Тестирование класса Vacancy
    """

    def test_vacancy_init(self):
        """
        Проверяет соответсвие имени класса реального и выводимого
        :return: ничего
        """
        self.assertEqual(type(Vacancy({'salary_from': '10',
                                       'salary_to': '100',
                                       'salary_gross': 'Без вычета налогов',
                                       'salary_currency': 'RUR',
                                       'name': 'Программист',
                                       'description': 'Настоящий мегамозг',
                                       'key_skills': 'Усидчивость',
                                       'experience_id': 'moreThan6',
                                       'premium': 'True',
                                       'employer_name': 'Скб Контур',
                                       'area_name': 'Екб',
                                       'published_at': '2022-05-31T17:32:31+0300'})).__name__, 'Vacancy')


if __name__ == 'main':
    main()