from unittest import TestCase, main
from function_in_OOP import DataSet


class DataSetTest(TestCase):
    """
    Тестирование класса DataSet
    """
    def test_dataset_type(self):
        """
        Проверяет соответсвие нcзывния файла получаемого и выводимого
        :return: ничего
        """
        self.assertEqual(DataSet('vacancies_medium.csv', 'Опыт работы: От 3 до 6 лет',
                                      'Оклад', 'Нет', '10 20').file_name, 'vacancies_medium.csv')

    def test_dataset_filter_param(self):
        """
        Проверяет соответсвие аргумента фильтрации получаемого и выводимого
        :return: ничего
        """
        self.assertEqual(DataSet('vacancies_medium.csv', 'Опыт работы: От 3 до 6 лет',
                                      'Оклад', 'Нет', '10 20').filter_param, 'Опыт работы: От 3 до 6 лет')

    def test_dataset_sort_param(self):
        """
        Проверяет соответсвие сортируемого аргумента получаемого и выводимого
        :return: ничего
        """
        self.assertEqual(DataSet('vacancies_medium.csv', 'Опыт работы: От 3 до 6 лет',
                                      'Оклад', 'Нет', '10 20').sort_param, 'Оклад')

    def test_dataset_sort_reverse(self):
        """
        Проверяет соответствие реверсируемого аргумента сортировки получаемого и выводимого
        :return: ничего
        """
        self.assertEqual(DataSet('vacancies_medium.csv', 'Опыт работы: От 3 до 6 лет',
                                      'Оклад', 'Нет', '10 20').sort_reverse, 'Нет')

    def test_dataset_sort_range(self):
        """
        Проверяет соответствие получаемого и выводимого аргумента,отвечающего за строчный промежуток вывода таблицы
        :return:
        """
        self.assertEqual(DataSet('vacancies_medium.csv', 'Опыт работы: От 3 до 6 лет',
                                      'Оклад', 'Нет', '10 20').sort_range, '10 20')


if __name__ == 'main':
    main()